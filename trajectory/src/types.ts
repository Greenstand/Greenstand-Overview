export interface LatLon {
  lat: number;
  lon: number;
}

export interface RawCapture {
  id: string | number;
  timestamp: string | Date;
  lat: number;
  lon: number;
  deviceId?: string;
}

export interface ScrubbedCapture extends RawCapture {
  isOutlier: boolean;
  anomalyReason?: string;
  impliedSpeedMps?: number;
  estimatedLocation: LatLon;
}

export interface DeviceAnomalyStat {
  deviceId: string;
  total: number;
  anomalyCount: number;
  jumpPercentage: number;
}

export interface ScrubOptions {
  maxSpeedMps?: number;
}

export const DEFAULT_MAX_SPEED_MPS = 2.5;
