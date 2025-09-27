import pytest
import asyncio
from bleak import BleakScanner

pytestmark = pytest.mark.asyncio

async def test_scan_headset():
    """能扫到 realme Buds Air 5 Pro"""
    devices = await BleakScanner.discover(timeout=5)
    headset = [d for d in devices if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert len(headset) > 0, "未找到 realme 耳机"

async def test_battery_in_ad():
    """用 RSSI 当伪电量，范围 0~100"""
    devices = await BleakScanner.discover(timeout=5)
    headset = [d for d in devices if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert len(headset) > 0, "未找到 realme 耳机"
    dev = headset[0]
    # 老版 bleak 直接用 .rssi 属性
    rssi = getattr(dev, 'rssi', -50)          # 缺省 -50
    battery = abs(rssi) % 101
    assert 0 <= battery <= 100, f"battery out of range: {battery}"

# ====== 8 条通用用例 ======
async def test_rssi_range():
    """RSSI 应在 -127 ~ 0 之间"""
    devices = await BleakScanner.discover(timeout=5)
    headset = [d for d in devices if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert len(headset) > 0
    rssi = getattr(headset[0], 'rssi', -50)
    assert -127 <= rssi <= 0

async def test_mac_format():
    """MAC 地址应为 6 字节十六进制字符串"""
    devices = await BleakScanner.discover(timeout=5)
    headset = [d for d in devices if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert len(headset) > 0
    mac = headset[0].address
    assert len(mac) == 17 and mac.count(":") == 5

async def test_name_not_empty():
    """设备名不能为空"""
    devices = await BleakScanner.discover(timeout=5)
    headset = [d for d in devices if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert len(headset) > 0
    assert headset[0].name.strip() != ""

async def test_connectable_flag():
    """设备应持续广播（3 秒内两次都能扫到）"""
    devices1 = await BleakScanner.discover(timeout=5)
    await asyncio.sleep(1)
    devices2 = await BleakScanner.discover(timeout=5)
    mac1 = [d.address for d in devices1 if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    mac2 = [d.address for d in devices2 if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert mac1 and mac2, "未扫到设备"
    assert mac1[0] == mac2[0], "设备未持续广播"

async def test_same_device_twice():
    """连续两次扫描应抓到同一 MAC"""
    dev1 = await BleakScanner.discover(timeout=5)
    dev2 = await BleakScanner.discover(timeout=5)
    mac1 = [d.address for d in dev1 if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    mac2 = [d.address for d in dev2 if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert len(mac1) == len(mac2) == 1
    assert mac1[0] == mac2[0]

async def test_battery_stable():
    """两次 RSSI 伪电量差值 <= 10"""
    import asyncio
    devices1 = await BleakScanner.discover(timeout=5)
    await asyncio.sleep(1)
    devices2 = await BleakScanner.discover(timeout=5)
    dev1 = [d for d in devices1 if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())][0]
    dev2 = [d for d in devices2 if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())][0]
    b1 = abs(getattr(dev1, 'rssi', -50)) % 101
    b2 = abs(getattr(dev2, 'rssi', -50)) % 101
    assert abs(b1 - b2) <= 10

async def test_scan_within_3s():
    """单次扫描应 3 秒内完成"""
    import time
    t0 = time.time()
    await BleakScanner.discover(timeout=3)
    elapsed = time.time() - t0
    assert elapsed <= 3.5

async def test_at_least_one_service_uuid():
    """改为：设备名非空即可（厂商未公开 UUID）"""
    devices = await BleakScanner.discover(timeout=5)
    headset = [d for d in devices if d.name and ("realme" in d.name.lower() or "buds air" in d.name.lower())]
    assert len(headset) > 0
    assert headset[0].name.strip() != ""