import { detectPlantingClusters } from "../src/clustering/STDBSCAN";
import { haversineDistance } from "../src/clustering/geoUtils";
import { TreeCapture } from "../src/clustering/types";

const origin = { lat: 8.48, lon: -13.27 };
const metersToLatitude = (meters: number): number => meters / 111_320;

function capture(
  id: string,
  eastMeters: number,
  northMeters: number,
  timestamp: string,
): TreeCapture {
  return {
    id,
    lat: origin.lat + metersToLatitude(northMeters),
    lon: origin.lon + metersToLatitude(eastMeters) / Math.cos((origin.lat * Math.PI) / 180),
    timestamp,
  };
}

describe("ST-DBSCAN planting-unit detection", () => {
  it("keeps a curved roadside campaign as one non-convex-friendly cluster", () => {
    const captures = Array.from({ length: 20 }, (_, index) => {
      const angle = index / 4;
      return capture(`road-${index}`, 30 * index, 80 * Math.sin(angle), `2026-03-01T${String(8 + Math.floor(index / 5)).padStart(2, "0")}:00:00Z`);
    });
    const result = detectPlantingClusters(captures, { spatialEpsMeters: 45, temporalEpsHours: 4, minPts: 3 });
    expect(result.clusters).toHaveLength(1);
    expect(result.clusters[0].size).toBe(20);
    expect(result.clusters[0].durationHours).toBe(3);
  });

  it("separates identical spatial grids planted months apart", () => {
    const first = Array.from({ length: 10 }, (_, index) => capture(`march-${index}`, index * 4, (index % 2) * 4, "2026-03-01T09:00:00Z"));
    const second = Array.from({ length: 10 }, (_, index) => capture(`september-${index}`, index * 4, (index % 2) * 4, "2026-09-01T09:00:00Z"));
    const result = detectPlantingClusters([...first, ...second], { spatialEpsMeters: 20, temporalEpsHours: 48, minPts: 3 });
    expect(result.clusters).toHaveLength(2);
    expect(result.clusters.map((cluster) => cluster.size)).toEqual([10, 10]);
  });

  it("separates synchronous campaigns ten kilometres apart", () => {
    const first = Array.from({ length: 10 }, (_, index) => capture(`a-${index}`, index * 3, 0, "2026-06-01T14:00:00Z"));
    const second = Array.from({ length: 10 }, (_, index) => capture(`b-${index}`, 10_000 + index * 3, 0, "2026-06-01T14:00:00Z"));
    const result = detectPlantingClusters([...first, ...second], { spatialEpsMeters: 25, temporalEpsHours: 2, minPts: 3 });
    expect(result.clusters).toHaveLength(2);
  });

  it("returns isolated plantings as noise", () => {
    const campaign = [capture("campaign-0", 0, 0, "2026-06-01T14:00:00Z"), capture("campaign-1", 5, 0, "2026-06-01T14:00:00Z"), capture("campaign-2", 10, 0, "2026-06-01T14:00:00Z")];
    const result = detectPlantingClusters([...campaign, capture("isolated", 2_000, 2_000, "2026-06-01T14:00:00Z")], { spatialEpsMeters: 20, temporalEpsHours: 2, minPts: 3 });
    expect(result.clusters[0].captureIds).toEqual(["campaign-0", "campaign-1", "campaign-2"]);
    expect(result.noiseCaptureIds).toEqual(["isolated"]);
  });

  it("handles empty, singleton, duplicate, and invalid inputs", () => {
    expect(detectPlantingClusters([])).toEqual({ clusters: [], noiseCaptureIds: [], totalProcessed: 0 });
    const same = capture("same", 0, 0, "2026-06-01T14:00:00Z");
    expect(detectPlantingClusters([same], { minPts: 1 }).clusters[0].centroid).toEqual({ lat: same.lat, lon: same.lon });
    expect(detectPlantingClusters([same, { ...same, id: "invalid", lat: Number.NaN }]).totalProcessed).toBe(1);
    expect(haversineDistance(0, 0, 0, 0)).toBe(0);
  });

  it("rejects invalid algorithm options", () => {
    expect(() => detectPlantingClusters([], { spatialEpsMeters: 0 })).toThrow(/spatialEpsMeters/);
    expect(() => detectPlantingClusters([], { minPts: 1.5 })).toThrow(/minPts/);
  });
});
