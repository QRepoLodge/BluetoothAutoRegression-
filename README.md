# Bluetooth Auto Regression (10 Cases)
Local BLE device auto-test demo based on `pytest + bleak + allure`.

## Environment
- Python 3.11+
- bleak 0.20+
- pytest 8.x
- allure-pytest

## Run
```bash
pip install -r requirements.txt
pytest -v --alluredir=results
allure serve results

沉默不是优雅  13:04:30
## 10 Cases Covered
1. `test_scan_headset` - 设备可被发现  
2. `test_battery_in_ad` - RSSI 转伪电量 0-100  
3. `test_rssi_range` - RSSI 范围校验  
4. `test_mac_format` - MAC 地址格式检查  
5. `test_name_not_empty` - 设备名非空  
6. `test_same_device_twice` - 重复扫描一致性  
7. `test_battery_stable` - 电量稳定性  
8. `test_scan_within_3s` - 扫描耗时 ≤ 3 秒  
9. `test_connectable_flag` - 广播持续可见  
10. `test_at_least_one_service_uuid` - 服务 UUID 存在（降级）

