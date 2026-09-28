import {
  computeCentroid,
  haversineDistance,
  METERS_PER_DEGREE,
  temporalDeltaHours,
} from "./geoUtils";
import {
  ClusteringResult,
  PlantingCluster,
  STDBSCANOptions,
  TreeCapture,
} from "./types";

interface NormalizedCapture extends TreeCapture {
  timestamp: Date;
  originalIndex: number;
}

interface IndexedCapture {
  capture: NormalizedCapture;
  cellLat: number;
  cellLon: number;
}

const DEFAULTS = {
  spatialEpsMeters: 250,
  temporalEpsHours: 48,
  minPts: 3,
} as const;

function parseCapture(capture: TreeCapture, originalIndex: number): NormalizedCapture | null {
  if (!Number.isFinite(capture.lat) || !Number.isFinite(capture.lon)
    || capture.lat < -90 || capture.lat > 90
    || capture.lon < -180 || capture.lon > 180) {
    return null;
  }
  const timestamp = new Date(capture.timestamp);
  if (Number.isNaN(timestamp.getTime())) {
    return null;
  }
  return {
    ...capture,
    lon: capture.lon === 180 ? 180 : capture.lon,
    timestamp,
    originalIndex,
  };
}

function validateOptions(options: Required<STDBSCANOptions>): void {
  if (!Number.isFinite(options.spatialEpsMeters) || options.spatialEpsMeters <= 0) {
    throw new Error("spatialEpsMeters must be a positive finite number");
  }
  if (!Number.isFinite(options.temporalEpsHours) || options.temporalEpsHours <= 0) {
    throw new Error("temporalEpsHours must be a positive finite number");
  }
  if (!Number.isInteger(options.minPts) || options.minPts < 1) {
    throw new Error("minPts must be a positive integer");
  }
}

export function detectPlantingClusters(
  captures: TreeCapture[],
  options: STDBSCANOptions = {},
): ClusteringResult {
  const resolved: Required<STDBSCANOptions> = {
    spatialEpsMeters: options.spatialEpsMeters ?? DEFAULTS.spatialEpsMeters,
    temporalEpsHours: options.temporalEpsHours ?? DEFAULTS.temporalEpsHours,
    minPts: options.minPts ?? DEFAULTS.minPts,
  };
  validateOptions(resolved);

  const normalized = captures
    .map((capture, index) => parseCapture(capture, index))
    .filter((capture): capture is NormalizedCapture => capture !== null);
  if (normalized.length === 0) {
    return { clusters: [], noiseCaptureIds: [], totalProcessed: 0 };
  }

  const cellSizeDegrees = resolved.spatialEpsMeters / METERS_PER_DEGREE;
  const longitudeCellCount = Math.ceil(360 / cellSizeDegrees);
  const buckets = new Map<string, number[]>();
  const indexed: IndexedCapture[] = normalized.map((capture, index) => {
    const cellLat = Math.floor((capture.lat + 90) / cellSizeDegrees);
    const cellLon = Math.min(
      longitudeCellCount - 1,
      Math.floor((capture.lon + 180) / cellSizeDegrees),
    );
    const item: IndexedCapture = { capture, cellLat, cellLon };
    const key = `${cellLat}:${cellLon}`;
    const bucket = buckets.get(key);
    if (bucket) bucket.push(index);
    else buckets.set(key, [index]);
    return item;
  });

  const region = (pointIndex: number): number[] => {
    const point = indexed[pointIndex];
    const latitudeRadians = (point.capture.lat * Math.PI) / 180;
    const longitudeSpan = Math.max(
      1,
      Math.ceil(1 / Math.max(Math.abs(Math.cos(latitudeRadians)), 1e-6)),
    );
    const candidates = new Set<number>();
    for (let latOffset = -1; latOffset <= 1; latOffset += 1) {
      for (let lonOffset = -longitudeSpan; lonOffset <= longitudeSpan; lonOffset += 1) {
        let cellLon = (point.cellLon + lonOffset) % longitudeCellCount;
        if (cellLon < 0) cellLon += longitudeCellCount;
        const bucket = buckets.get(`${point.cellLat + latOffset}:${cellLon}`);
        if (bucket) bucket.forEach((candidate) => candidates.add(candidate));
      }
    }
    return [...candidates].filter((candidate) => {
      const other = indexed[candidate].capture;
      return haversineDistance(point.capture.lat, point.capture.lon, other.lat, other.lon)
        <= resolved.spatialEpsMeters
        && temporalDeltaHours(point.capture.timestamp, other.timestamp)
        <= resolved.temporalEpsHours;
    });
  };

  const visited = new Set<number>();
  const noise = new Set<number>();
  const assigned = new Set<number>();
  const clusterIndexes: number[][] = [];

  for (let index = 0; index < indexed.length; index += 1) {
    if (visited.has(index)) continue;
    visited.add(index);
    const neighbors = region(index);
    if (neighbors.length < resolved.minPts) {
      noise.add(index);
      continue;
    }

    const cluster: number[] = [];
    const queue = [...neighbors];
    const queued = new Set(queue);
    assigned.add(index);
    cluster.push(index);
    for (let cursor = 0; cursor < queue.length; cursor += 1) {
      const candidate = queue[cursor];
      if (!visited.has(candidate)) {
        visited.add(candidate);
        const candidateNeighbors = region(candidate);
        if (candidateNeighbors.length >= resolved.minPts) {
          for (const neighbor of candidateNeighbors) {
            if (!queued.has(neighbor)) {
              queued.add(neighbor);
              queue.push(neighbor);
            }
          }
        }
      }
      noise.delete(candidate);
      if (!assigned.has(candidate)) {
        assigned.add(candidate);
        cluster.push(candidate);
      }
    }
    clusterIndexes.push(cluster);
  }

  const clusters = clusterIndexes.map((indexes, clusterNumber) => buildCluster(indexes, indexed, clusterNumber));
  const noiseCaptureIds = [...noise]
    .sort((left, right) => indexed[left].capture.originalIndex - indexed[right].capture.originalIndex)
    .map((index) => indexed[index].capture.id);
  return { clusters, noiseCaptureIds, totalProcessed: normalized.length };
}

function buildCluster(
  indexes: number[],
  indexed: IndexedCapture[],
  clusterNumber: number,
): PlantingCluster {
  const captures = indexes.map((index) => indexed[index].capture);
  const chronological = [...captures].sort((first, second) => (
    first.timestamp.getTime() - second.timestamp.getTime()
      || first.originalIndex - second.originalIndex
  ));
  const latitudes = captures.map((capture) => capture.lat);
  const longitudes = captures.map((capture) => capture.lon);
  const start = chronological[0].timestamp;
  const end = chronological[chronological.length - 1].timestamp;
  const stepDistances = chronological.slice(1).map((capture, index) => (
    haversineDistance(
      chronological[index].lat,
      chronological[index].lon,
      capture.lat,
      capture.lon,
    )
  ));
  return {
    clusterId: `planting-${clusterNumber + 1}`,
    captureIds: captures
      .sort((first, second) => first.originalIndex - second.originalIndex)
      .map((capture) => capture.id),
    size: captures.length,
    centroid: computeCentroid(captures),
    boundingBox: {
      minLat: Math.min(...latitudes),
      maxLat: Math.max(...latitudes),
      minLon: Math.min(...longitudes),
      maxLon: Math.max(...longitudes),
    },
    timeRange: { start: new Date(start), end: new Date(end) },
    durationHours: (end.getTime() - start.getTime()) / 3_600_000,
    meanStepDistanceMeters: stepDistances.length === 0
      ? 0
      : stepDistances.reduce((sum, distance) => sum + distance, 0) / stepDistances.length,
  };
}
