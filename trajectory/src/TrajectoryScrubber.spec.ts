import { haversineDistance } from './kinematics';
import { getDeviceAnomalyStats, scrubSessionCaptures } from './TrajectoryScrubber';
import { RawCapture } from './types';

const DAY = '2020-06-13T';

function capture(
  id: string,
  clock: string,
  lat: number,
  lon: number,
  deviceId = 'phone-a',
): RawCapture {
  return { id, timestamp: `${DAY}${clock}Z`, lat, lon, deviceId };
}

describe('scrubSessionCaptures', () => {
  test('flags the issue 155 ocean jump and keeps the estimate next to the walk', () => {
    // Ticket order is not chronological. Tree 2 is the bad fix.
    const raw: RawCapture[] = [
      capture('4', '14:45:03', 8.484414, -13.275778),
      capture('3', '14:41:32', 8.484348, -13.275916),
      capture('2', '14:40:03', 8.014978, -13.250369),
      capture('1', '16:39:00', 8.482369, -13.277495),
    ];

    const scrubbed = scrubSessionCaptures(raw);
    expect(scrubbed.map((row) => row.id)).toEqual(['2', '3', '4', '1']);

    const jumped = scrubbed[0];
    expect(jumped.isOutlier).toBe(true);
    expect(jumped.lat).toBe(8.014978);
    expect(jumped.lon).toBe(-13.250369);
    expect(jumped.impliedSpeedMps).toBeGreaterThan(100);

    const nearestInlier = scrubbed[1];
    const repaired = haversineDistance(
      jumped.estimatedLocation.lat,
      jumped.estimatedLocation.lon,
      nearestInlier.lat,
      nearestInlier.lon,
    );
    expect(repaired).toBeLessThan(30);

    for (const row of scrubbed.slice(1)) {
      expect(row.isOutlier).toBe(false);
      expect(row.estimatedLocation).toEqual({ lat: row.lat, lon: row.lon });
    }
  });

  test('leaves a walking pace sequence unmarked', () => {
    // ~1.1 m north each second, well under 1.5 m/s.
    const raw: RawCapture[] = [0, 1, 2, 3, 4].map((i) =>
      capture(String(i), `10:00:0${i}`, 8.48 + i * 0.00001, -13.27),
    );
    const scrubbed = scrubSessionCaptures(raw);
    expect(scrubbed.every((row) => !row.isOutlier)).toBe(true);
    expect(Math.max(...scrubbed.map((row) => row.impliedSpeedMps ?? 0))).toBeLessThan(1.5);
  });

  test('does not divide by zero when timestamps collide', () => {
    const same = '2020-06-13T10:00:00Z';
    const jitter: RawCapture[] = [
      { id: 'a', timestamp: same, lat: 8.48, lon: -13.27, deviceId: 'phone-a' },
      { id: 'b', timestamp: same, lat: 8.48, lon: -13.27, deviceId: 'phone-a' },
      { id: 'c', timestamp: new Date(Date.parse(same) + 1), lat: 8.480001, lon: -13.27, deviceId: 'phone-a' },
    ];
    expect(() => scrubSessionCaptures(jitter)).not.toThrow();
    const scrubbed = scrubSessionCaptures(jitter);
    expect(scrubbed.every((row) => !row.isOutlier)).toBe(true);
    expect(scrubbed.every((row) => Number.isFinite(row.impliedSpeedMps))).toBe(true);
  });

  test('repairs a run of jumps and an edge point from the enclosing walk', () => {
    const raw: RawCapture[] = [
      capture('edge', '09:00:00', 1.5, 30.5),
      capture('a', '10:00:00', 8.48, -13.27),
      capture('bad-1', '10:00:30', 8.9, -13.6),
      capture('bad-2', '10:01:00', 9.2, -14.1),
      capture('b', '10:02:00', 8.4802, -13.2701),
      capture('c', '10:03:00', 8.4804, -13.2702),
    ];

    const scrubbed = scrubSessionCaptures(raw);
    const byId = Object.fromEntries(scrubbed.map((row) => [row.id, row]));

    expect(byId.edge.isOutlier).toBe(true);
    expect(byId['bad-1'].isOutlier).toBe(true);
    expect(byId['bad-2'].isOutlier).toBe(true);
    expect(byId.a.isOutlier).toBe(false);
    expect(byId.b.isOutlier).toBe(false);

    expect(byId.edge.estimatedLocation).toEqual({ lat: byId.a.lat, lon: byId.a.lon });

    const span = Date.parse(String(byId.b.timestamp)) - Date.parse(String(byId.a.timestamp));
    const alpha = (Date.parse(String(byId['bad-1'].timestamp)) - Date.parse(String(byId.a.timestamp))) / span;
    const moved = haversineDistance(
      byId['bad-1'].estimatedLocation.lat,
      byId['bad-1'].estimatedLocation.lon,
      byId['bad-1'].lat,
      byId['bad-1'].lon,
    );
    expect(alpha).toBeGreaterThan(0);
    expect(alpha).toBeLessThan(1);
    expect(moved).toBeGreaterThan(1000);
    expect(
      haversineDistance(
        byId['bad-1'].estimatedLocation.lat,
        byId['bad-1'].estimatedLocation.lon,
        byId.a.lat,
        byId.a.lon,
      ),
    ).toBeLessThan(500);

    const stats = getDeviceAnomalyStats(scrubbed);
    expect(stats).toEqual([
      { deviceId: 'phone-a', total: 6, anomalyCount: 3, jumpPercentage: 50 },
    ]);
  });
});
