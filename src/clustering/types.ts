export interface TreeCapture {
  id: string | number;
  lat: number;
  lon: number;
  timestamp: string | Date;
  planterId?: string;
  species?: string;
}

export interface BoundingBox {
  minLat: number;
  maxLat: number;
  minLon: number;
  maxLon: number;
}

export interface PlantingCluster {
  clusterId: string;
  captureIds: Array<string | number>;
  size: number;
  centroid: { lat: number; lon: number };
  boundingBox: BoundingBox;
  timeRange: { start: Date; end: Date };
  durationHours: number;
  meanStepDistanceMeters: number;
}

export interface ClusteringResult {
  clusters: PlantingCluster[];
  noiseCaptureIds: Array<string | number>;
  totalProcessed: number;
}

export interface STDBSCANOptions {
  spatialEpsMeters?: number;
  temporalEpsHours?: number;
  minPts?: number;
}
