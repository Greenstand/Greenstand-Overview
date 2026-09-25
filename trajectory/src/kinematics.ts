import { LatLon } from './types';

const EARTH_RADIUS_M = 6371008.8;
const DEG = Math.PI / 180;

export function haversineDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
): number {
  const phi1 = lat1 * DEG;
  const phi2 = lat2 * DEG;
  const dPhi = (lat2 - lat1) * DEG;
  const dLambda = (lon2 - lon1) * DEG;
  const a =
    Math.sin(dPhi / 2) ** 2 +
    Math.cos(phi1) * Math.cos(phi2) * Math.sin(dLambda / 2) ** 2;
  return 2 * EARTH_RADIUS_M * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function toEcef(point: LatLon): [number, number, number] {
  const phi = point.lat * DEG;
  const lambda = point.lon * DEG;
  const cosPhi = Math.cos(phi);
  return [cosPhi * Math.cos(lambda), cosPhi * Math.sin(lambda), Math.sin(phi)];
}

function fromEcef(x: number, y: number, z: number): LatLon {
  const hyp = Math.sqrt(x * x + y * y);
  return {
    lat: Math.atan2(z, hyp) / DEG,
    lon: Math.atan2(y, x) / DEG,
  };
}

/** Point at `fraction` along the great-circle arc from p1 to p2. */
export function geodesicInterpolate(
  p1: LatLon,
  p2: LatLon,
  fraction: number,
): LatLon {
  const t = Math.min(1, Math.max(0, fraction));
  const v1 = toEcef(p1);
  const v2 = toEcef(p2);
  const dot = Math.min(1, Math.max(-1, v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]));
  const omega = Math.acos(dot);
  if (omega < 1e-12) {
    return { lat: p1.lat, lon: p1.lon };
  }
  const sinOmega = Math.sin(omega);
  const a = Math.sin((1 - t) * omega) / sinOmega;
  const b = Math.sin(t * omega) / sinOmega;
  return fromEcef(
    a * v1[0] + b * v2[0],
    a * v1[1] + b * v2[1],
    a * v1[2] + b * v2[2],
  );
}
