import { geodesicInterpolate, haversineDistance } from './kinematics';
import {
  DEFAULT_MAX_SPEED_MPS,
  DeviceAnomalyStat,
  LatLon,
  RawCapture,
  ScrubbedCapture,
  ScrubOptions,
} from './types';

const SAME_INSTANT_TOLERANCE_M = 1;
const JITTER_WINDOW_SEC = 0.05;
const JITTER_RADIUS_M = 30;

interface TimedCapture extends RawCapture {
  timeMs: number;
}

function parseTime(timestamp: string | Date): number {
  const ms = timestamp instanceof Date ? timestamp.getTime() : Date.parse(timestamp);
  if (Number.isNaN(ms)) {
    throw new Error(`unparseable timestamp: ${String(timestamp)}`);
  }
  return ms;
}

function stepSpeed(a: TimedCapture, b: TimedCapture): number | undefined {
  const dt = (b.timeMs - a.timeMs) / 1000;
  const distance = haversineDistance(a.lat, a.lon, b.lat, b.lon);
  if (dt <= 0) {
    return distance > SAME_INSTANT_TOLERANCE_M ? Number.POSITIVE_INFINITY : 0;
  }
  if (dt < JITTER_WINDOW_SEC && distance <= JITTER_RADIUS_M) return 0;
  return distance / dt;
}

function exceeds(speed: number | undefined, maxSpeedMps: number): boolean {
  return speed !== undefined && speed > maxSpeedMps;
}

/**
 * Longest time-ordered chain whose consecutive kept points stay under the
 * speed cap. Skipped points are the GPS jumps.
 */
function inlierIndices(points: TimedCapture[], maxSpeedMps: number): Set<number> {
  const n = points.length;
  const dp = new Array<number>(n).fill(1);
  const prev = new Array<number>(n).fill(-1);

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < i; j++) {
      const speed = stepSpeed(points[j], points[i]);
      if (!exceeds(speed, maxSpeedMps) && dp[j] + 1 > dp[i]) {
        dp[i] = dp[j] + 1;
        prev[i] = j;
      }
    }
  }

  let best = 0;
  for (let i = 1; i < n; i++) {
    if (dp[i] > dp[best]) best = i;
  }

  const keep = new Set<number>();
  for (let i = best; i !== -1; i = prev[i]) keep.add(i);
  return keep;
}

function neighborSpeed(points: TimedCapture[], index: number): number | undefined {
  const speeds: number[] = [];
  if (index > 0) {
    const left = stepSpeed(points[index - 1], points[index]);
    if (left !== undefined) speeds.push(left);
  }
  if (index < points.length - 1) {
    const right = stepSpeed(points[index], points[index + 1]);
    if (right !== undefined) speeds.push(right);
  }
  if (speeds.length === 0) return undefined;
  return Math.max(...speeds);
}

function repairLocation(
  points: TimedCapture[],
  index: number,
  inliers: Set<number>,
): LatLon {
  let prev = -1;
  let next = -1;
  for (let i = index - 1; i >= 0; i--) {
    if (inliers.has(i)) {
      prev = i;
      break;
    }
  }
  for (let i = index + 1; i < points.length; i++) {
    if (inliers.has(i)) {
      next = i;
      break;
    }
  }

  if (prev >= 0 && next >= 0) {
    const span = points[next].timeMs - points[prev].timeMs;
    const alpha = span > 0 ? (points[index].timeMs - points[prev].timeMs) / span : 0;
    return geodesicInterpolate(points[prev], points[next], alpha);
  }

  const anchor = prev >= 0 ? prev : next;
  if (anchor >= 0) {
    return { lat: points[anchor].lat, lon: points[anchor].lon };
  }
  return { lat: points[index].lat, lon: points[index].lon };
}

export function scrubSessionCaptures(
  captures: RawCapture[],
  options?: ScrubOptions,
): ScrubbedCapture[] {
  const maxSpeedMps = options?.maxSpeedMps ?? DEFAULT_MAX_SPEED_MPS;
  const points: TimedCapture[] = captures
    .map((capture) => ({ ...capture, timeMs: parseTime(capture.timestamp) }))
    .sort((a, b) => a.timeMs - b.timeMs || String(a.id).localeCompare(String(b.id)));

  if (points.length === 0) return [];

  const inliers = inlierIndices(points, maxSpeedMps);

  return points.map((point, index) => {
    const outlier = !inliers.has(index);
    const impliedSpeedMps = neighborSpeed(points, index);
    const estimatedLocation = outlier
      ? repairLocation(points, index, inliers)
      : { lat: point.lat, lon: point.lon };

    const scrubbed: ScrubbedCapture = {
      id: point.id,
      timestamp: point.timestamp,
      lat: point.lat,
      lon: point.lon,
      isOutlier: outlier,
      impliedSpeedMps,
      estimatedLocation,
    };
    if (point.deviceId !== undefined) scrubbed.deviceId = point.deviceId;
    if (outlier) {
      scrubbed.anomalyReason =
        impliedSpeedMps === Number.POSITIVE_INFINITY
          ? 'non-zero displacement at a repeated timestamp'
          : `implied speed ${impliedSpeedMps?.toFixed(1)} m/s exceeds ${maxSpeedMps} m/s`;
    }
    return scrubbed;
  });
}

export function getDeviceAnomalyStats(scrubbed: ScrubbedCapture[]): DeviceAnomalyStat[] {
  const buckets = new Map<string, { total: number; anomalyCount: number }>();
  for (const capture of scrubbed) {
    const deviceId = capture.deviceId ?? 'unknown';
    const bucket = buckets.get(deviceId) ?? { total: 0, anomalyCount: 0 };
    bucket.total += 1;
    if (capture.isOutlier) bucket.anomalyCount += 1;
    buckets.set(deviceId, bucket);
  }

  return [...buckets.entries()]
    .map(([deviceId, bucket]) => ({
      deviceId,
      total: bucket.total,
      anomalyCount: bucket.anomalyCount,
      jumpPercentage: bucket.total === 0 ? 0 : (bucket.anomalyCount / bucket.total) * 100,
    }))
    .sort((a, b) => a.deviceId.localeCompare(b.deviceId));
}
