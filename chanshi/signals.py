from blinker import Namespace

boot = Namespace()

booting = boot.signal('BOOTING')  # app启动时发送
after_boot = boot.signal('AFTER_BOOT')  # 启动完成后
