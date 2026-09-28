import { TreeCapture } from "./types";

const EARTH_RADIUS_METERS = 6_371_000;
const METERS_PER_DEGREE = (Math.PI * EARTH_RADIUS_METERS) / 180;

export function haversineDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
): number {
  const phi1 = (lat1 * Math.PI) / 180;
  const phi2 = (lat2 * Math.PI) / 180;
  const dPhi = ((lat2 - lat1) * Math.PI) / 180;
  const dLambda = ((lon2 - lon1) * Math.PI) / 180;
  const sine = Math.sin(dPhi / 2) ** 2
    + Math.cos(phi1) * Math.cos(phi2) * Math.sin(dLambda / 2) ** 2;
  const centralAngle = 2 * Math.asin(Math.sqrt(Math.min(1, Math.max(0, sine))));
  return EARTH_RADIUS_METERS * centralAngle;
}

export function temporalDeltaHours(first: Date, second: Date): number {
  return Math.abs(first.getTime() - second.getTime()) / 3_600_000;
}

export function computeCentroid(captures: TreeCapture[]): { lat: number; lon: number } {
  if (captures.length === 0) {
    throw new Error("Cannot compute a centroid for an empty capture set");
  }
  if (captures.length === 1) {
    return { lat: captures[0].lat, lon: captures[0].lon };
  }

  let x = 0;
  let y = 0;
  let z = 0;
  for (const capture of captures) {
    const latitude = (capture.lat * Math.PI) / 180;
    const longitude = (capture.lon * Math.PI) / 180;
    x += Math.cos(latitude) * Math.cos(longitude);
    y += Math.cos(latitude) * Math.sin(longitude);
    z += Math.sin(latitude);
  }

  const magnitude = Math.hypot(x, y, z);
  if (magnitude < Number.EPSILON) {
    return {
      lat: captures.reduce((sum, capture) => sum + capture.lat, 0) / captures.length,
      lon: captures.reduce((sum, capture) => sum + capture.lon, 0) / captures.length,
    };
  }

  return {
    lat: (Math.atan2(z, Math.hypot(x, y)) * 180) / Math.PI,
    lon: (Math.atan2(y, x) * 180) / Math.PI,
  };
}

export { EARTH_RADIUS_METERS, METERS_PER_DEGREE };
