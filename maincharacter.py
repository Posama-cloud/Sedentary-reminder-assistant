import rumps
import cv2
import time
import os
import threading
import subprocess
import logging
import json
from datetime import datetime

# --- 配置 ---
APP_ICON_PATH = "image_0.png"

# 默认间隔：3600 秒（1小时）
DEFAULT_INTERVAL_SECONDS = 3600

# 点击「我知道了」后，等待多少秒再做第二次确认检测
CONFIRM_DELAY_SECONDS = 30

# 第二次确认时，连拍多少帧来判断是否有人（取多数结果，避免单帧误判）
CONFIRM_FRAMES = 5

# --- 配置文件路径 ---
CONFIG_DIR = os.path.expanduser("~/.sedentary_reminder")
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
STATS_FILE = os.path.join(CONFIG_DIR, "stats.json")

# --- 日志配置 ---
LOG_DIR = os.path.expanduser("~/Library/Logs/久坐提醒助手")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ===================================================================
#  配置管理类
# ===================================================================
class Config:
    """配置管理类"""
    
    @staticmethod
    def load():
        """加载配置"""
        default_config = {
            "interval_seconds": DEFAULT_INTERVAL_SECONDS,
            "show_welcome": True,
            "confirm_delay": CONFIRM_DELAY_SECONDS
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                logger.error(f"加载配置失败: {e}")
                return default_config
        return default_config
    
    @staticmethod
    def save(config):
        """保存配置"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            logger.info(f"配置已保存")
        except Exception as e:
            logger.error(f"保存配置失败: {e}")


# ===================================================================
#  统计数据管理类
# ===================================================================
class Stats:
    """统计数据管理类"""
    
    @staticmethod
    def load():
        """加载统计数据"""
        default_stats = {
            "total_reminders": 0,
            "total_activities": 0,
            "total_ignored": 0,
            "today_reminders": 0,
            "today_activities": 0,
            "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
            "history": []
        }
        
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                    # 检查是否需要重置今日数据
                    today = datetime.now().strftime("%Y-%m-%d")
                    if stats.get("last_reset_date") != today:
                        stats["today_reminders"] = 0
                        stats["today_activities"] = 0
                        stats["last_reset_date"] = today
                    return {**default_stats, **stats}
            except Exception as e:
                logger.error(f"加载统计数据失败: {e}")
                return default_stats
        return default_stats
    
    @staticmethod
    def save(stats):
        """保存统计数据"""
        try:
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存统计数据失败: {e}")
    
    @staticmethod
    def add_reminder(stats):
        """记录一次提醒"""
        stats["total_reminders"] += 1
        stats["today_reminders"] += 1
        stats["history"].append({
            "type": "reminder",
            "time": datetime.now().isoformat()
        })
        if len(stats["history"]) > 100:
            stats["history"] = stats["history"][-100:]
        return stats
    
    @staticmethod
    def add_activity(stats):
        """记录一次活动"""
        stats["total_activities"] += 1
        stats["today_activities"] += 1
        stats["history"].append({
            "type": "activity",
            "time": datetime.now().isoformat()
        })
        if len(stats["history"]) > 100:
            stats["history"] = stats["history"][-100:]
        return stats
    
    @staticmethod
    def add_ignored(stats):
        """记录一次忽略"""
        stats["total_ignored"] += 1
        stats["history"].append({
            "type": "ignored",
            "time": datetime.now().isoformat()
        })
        if len(stats["history"]) > 100:
            stats["history"] = stats["history"][-100:]
        return stats


class SedentaryReminderApp(rumps.App):
    def __init__(self):
        logger.info("=" * 60)
        logger.info("久坐提醒助手启动 v1.1")
        logger.info("=" * 60)
        
        if os.path.exists(APP_ICON_PATH):
            super(SedentaryReminderApp, self).__init__("", icon=APP_ICON_PATH)
            logger.info(f"使用图标: {APP_ICON_PATH}")
        else:
            super(SedentaryReminderApp, self).__init__("久坐")
            logger.warning(f"图标文件不存在: {APP_ICON_PATH}")

        # 加载配置和统计数据
        self.config = Config.load()
        self.stats = Stats.load()
        logger.info(f"配置已加载: 间隔 {self.config['interval_seconds']} 秒")
        logger.info(f"统计数据: 总提醒 {self.stats['total_reminders']} 次")
        
        # 创建菜单
        self.title_item = rumps.MenuItem("久坐提醒：初始化中…", callback=None)
        
        # 创建设置子菜单
        self.interval_menu = rumps.MenuItem("设置提醒间隔")
        
        self.menu = [
            self.interval_menu,
            rumps.separator,
            "重置计时器",
            "立即测试检测",
            "查看统计",
            "查看日志",
            "关于",
            rumps.separator,
            self.title_item
        ]
        
        # 添加间隔子菜单项
        self.interval_30min = rumps.MenuItem("30 分钟", callback=self.set_interval_30)
        self.interval_45min = rumps.MenuItem("45 分钟", callback=self.set_interval_45)
        self.interval_1hour = rumps.MenuItem("1 小时", callback=self.set_interval_1hour)
        self.interval_2hour = rumps.MenuItem("2 小时", callback=self.set_interval_2hour)
        self.interval_custom = rumps.MenuItem("自定义...", callback=self.set_interval_custom)
        
        self.interval_menu.add(self.interval_30min)
        self.interval_menu.add(self.interval_45min)
        self.interval_menu.add(self.interval_1hour)
        self.interval_menu.add(self.interval_2hour)
        self.interval_menu.add(rumps.separator)
        self.interval_menu.add(self.interval_custom)
        
        # 更新当前选中的间隔
        self._update_interval_checkmarks()

        # 下次触发提醒的目标时间戳
        self.next_alert_time = time.time() + self.config["interval_seconds"]
        self.is_detecting = False

        # 初始化人脸检测器
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        logger.info(f"加载人脸检测器: {cascade_path}")
        
        if not os.path.exists(cascade_path):
            logger.error(f"人脸检测器文件不存在: {cascade_path}")
            rumps.alert(
                title="初始化失败",
                message=f"找不到人脸检测器文件。\n请检查 OpenCV 安装是否完整。\n\n日志位置: {LOG_FILE}",
                ok="确定"
            )
        
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            logger.error("人脸检测器加载失败")
            rumps.alert(
                title="初始化失败",
                message=f"人脸检测器加载失败。\n请重新安装 opencv-python。\n\n日志位置: {LOG_FILE}",
                ok="确定"
            )

        # 启动前检查并展示欢迎语
        self.check_and_show_welcome()

        # 使用 rumps.timer 启动定时器
        self.timer = rumps.Timer(self.update_countdown, 1)
        self.timer.start()
        
        logger.info("初始化完成")

    # ------------------------------------------------------------------ #
    #  首次启动欢迎弹窗
    # ------------------------------------------------------------------ #
    def check_and_show_welcome(self):
        if not self.config.get("show_welcome", True):
            logger.info("跳过欢迎提示")
            return

        logger.info("显示欢迎提示")
        response = rumps.alert(
            title="欢迎使用久坐提醒助手",
            message=f"程序将定期检测摄像头，提醒您起来活动。\n\n当前提醒间隔: {self._format_interval(self.config['interval_seconds'])}\n\n您可以在菜单中自定义提醒间隔和查看统计数据。\n\n日志位置: {LOG_FILE}",
            ok="开始使用",
            cancel="不再显示",
            icon_path=APP_ICON_PATH if os.path.exists(APP_ICON_PATH) else None
        )

        if response == 0:
            self.config["show_welcome"] = False
            Config.save(self.config)
            logger.info("用户选择不再显示欢迎提示")

    # ------------------------------------------------------------------ #
    #  设置提醒间隔
    # ------------------------------------------------------------------ #
    def _format_interval(self, seconds):
        """格式化时间间隔"""
        if seconds >= 3600:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes > 0:
                return f"{hours} 小时 {minutes} 分钟"
            return f"{hours} 小时"
        else:
            minutes = seconds // 60
            return f"{minutes} 分钟"
    
    def _update_interval_checkmarks(self):
        """更新间隔菜单的勾选状态"""
        current = self.config["interval_seconds"]
        self.interval_30min.state = (current == 1800)
        self.interval_45min.state = (current == 2700)
        self.interval_1hour.state = (current == 3600)
        self.interval_2hour.state = (current == 7200)
    
    def _set_interval(self, seconds):
        """设置提醒间隔"""
        self.config["interval_seconds"] = seconds
        Config.save(self.config)
        self._update_interval_checkmarks()
        self.next_alert_time = time.time() + seconds
        logger.info(f"提醒间隔已设置为: {self._format_interval(seconds)}")
        rumps.notification(
            title="设置已更新",
            subtitle=f"提醒间隔: {self._format_interval(seconds)}",
            message="计时器已重置"
        )
    
    def set_interval_30(self, sender):
        self._set_interval(1800)
    
    def set_interval_45(self, sender):
        self._set_interval(2700)
    
    def set_interval_1hour(self, sender):
        self._set_interval(3600)
    
    def set_interval_2hour(self, sender):
        self._set_interval(7200)
    
    def set_interval_custom(self, sender):
        """自定义间隔"""
        # 使用 AppleScript 创建更简洁的输入框
        applescript = '''
        try
            set userInput to text returned of (display dialog "请输入提醒间隔（分钟）：" default answer "60" buttons {"取消", "确定"} default button "确定" with title "自定义提醒间隔")
            return userInput
        on error
            return "CANCELLED"
        end try
        '''
        
        try:
            output = subprocess.check_output(
                ['osascript', '-e', applescript],
                stderr=subprocess.PIPE
            ).decode('utf-8').strip()
            
            if output == "CANCELLED":
                return
            
            try:
                minutes = int(output)
                if minutes <= 0:
                    rumps.alert("输入错误", "请输入大于 0 的数字")
                    return
                if minutes > 480:
                    rumps.alert("输入错误", "提醒间隔不能超过 8 小时（480 分钟）")
                    return
                
                seconds = minutes * 60
                self._set_interval(seconds)
            except ValueError:
                rumps.alert("输入错误", "请输入有效的数字")
                
        except Exception as e:
            logger.error(f"自定义间隔设置失败: {e}", exc_info=True)

    # ------------------------------------------------------------------ #
    #  统计功能
    # ------------------------------------------------------------------ #
    @rumps.clicked("查看统计")
    def show_stats(self, sender):
        """显示统计信息"""
        logger.info("显示统计信息")
        
        stats = self.stats
        activity_rate = self._calculate_activity_rate()
        
        message = f"""📊 使用统计

今日数据：
  • 提醒次数：{stats['today_reminders']} 次
  • 活动次数：{stats['today_activities']} 次

累计数据：
  • 总提醒次数：{stats['total_reminders']} 次
  • 总活动次数：{stats['total_activities']} 次
  • 总忽略次数：{stats['total_ignored']} 次

活动率：{activity_rate}%
（活动率 = 活动次数 / 提醒次数）

数据文件：{STATS_FILE}"""
        
        rumps.alert(
            title="使用统计",
            message=message,
            ok="确定"
        )
    
    def _calculate_activity_rate(self):
        """计算活动率"""
        total = self.stats['total_reminders']
        if total == 0:
            return 0
        activities = self.stats['total_activities']
        return round((activities / total) * 100, 1)

    # ------------------------------------------------------------------ #
    #  菜单栏操作
    # ------------------------------------------------------------------ #
    @rumps.clicked("重置计时器")
    def reset_timer(self, _):
        logger.info("用户手动重置计时器")
        self.next_alert_time = time.time() + self.config["interval_seconds"]
        self.title_item.title = "久坐提醒：已重置，重新倒计时"

    @rumps.clicked("立即测试检测")
    def test_detection(self, _):
        logger.info("用户触发立即测试")
        self.title_item.title = "久坐提醒：测试检测中…"
        
        # 在新线程中执行检测，避免阻塞UI
        def run_test():
            try:
                person_present = self._detect_person()
                result = "检测到有人" if person_present else "未检测到人"
                logger.info(f"测试结果: {result}")
                
                # 使用 rumps.notification 而不是 alert，避免阻塞
                rumps.notification(
                    title="检测测试结果",
                    subtitle=result,
                    message=f"详细日志请查看: {LOG_FILE}"
                )
                self.title_item.title = f"久坐提醒：测试完成 - {result}"
            except Exception as e:
                logger.error(f"测试检测失败: {e}", exc_info=True)
                rumps.notification(
                    title="测试失败",
                    subtitle="检测过程出错",
                    message=f"详细日志: {LOG_FILE}"
                )
        
        threading.Thread(target=run_test, daemon=True).start()

    @rumps.clicked("查看日志")
    def open_log(self, _):
        logger.info("用户打开日志文件")
        subprocess.run(['open', LOG_FILE])

    @rumps.clicked("关于")
    def about_app(self, _):
        logger.info("显示关于信息")
        rumps.alert(
            title="久坐提醒助手 v1.1",
            message=f"一个通过摄像头检测您是否久坐的工具。\n\n✨ v1.1 新功能：\n  • 自定义提醒间隔\n  • 使用统计\n  • 更友好的提醒方式\n\n日志位置: {LOG_FILE}\n配置文件: {CONFIG_FILE}",
            icon_path=APP_ICON_PATH if os.path.exists(APP_ICON_PATH) else None,
            ok="好的"
        )

    # ------------------------------------------------------------------ #
    #  主循环（倒计时 + 定时触发检测）
    # ------------------------------------------------------------------ #
    def update_countdown(self, sender):
        """
        定时器回调函数，每秒调用一次（在主线程中运行）
        """
        try:
            # 如果正在检测中，不更新倒计时
            if self.is_detecting:
                return
            
            remaining = self.next_alert_time - time.time()

            if remaining > 0:
                # 更新菜单栏倒计时显示
                self._update_countdown_display(remaining)
            else:
                # 到点了，执行一次检测流程（在后台线程中）
                logger.info("倒计时结束，开始检测流程")
                self.is_detecting = True
                threading.Thread(target=self._run_detection_cycle, daemon=True).start()
                
        except Exception as e:
            logger.error(f"更新倒计时出错: {e}", exc_info=True)
            self.title_item.title = f"久坐提醒：出错了，请查看日志"

    def _update_countdown_display(self, remaining_seconds):
        """更新倒计时显示（在主线程中调用）"""
        remaining = int(remaining_seconds)
        if remaining >= 3600:
            h = remaining // 3600
            m = (remaining % 3600) // 60
            title = f"久坐提醒：还有 {h} 小时 {m} 分"
        elif remaining >= 60:
            m = remaining // 60
            s = remaining % 60
            title = f"久坐提醒：还有 {m} 分 {s} 秒"
        else:
            title = f"久坐提醒：还有 {remaining} 秒"
        
        self.title_item.title = title

    # ------------------------------------------------------------------ #
    #  检测循环
    # ------------------------------------------------------------------ #
    def _run_detection_cycle(self):
        """到点后的完整检测+提醒流程（在后台线程中运行）。"""
        logger.info("开始检测周期")
        self.title_item.title = "久坐提醒：检测中…"

        try:
            person_present = self._detect_person()
            logger.info(f"初次检测结果: {'有人' if person_present else '无人'}")

            if not person_present:
                # 没人，直接重置倒计时
                logger.info("未检测到人，重置倒计时")
                self.stats = Stats.add_activity(self.stats)
                Stats.save(self.stats)
                self._reset_countdown()
                return

            # 有人，记录提醒并发送通知
            logger.info("检测到有人，发送提醒")
            self.stats = Stats.add_reminder(self.stats)
            Stats.save(self.stats)
            
            user_choice = self.send_reminder_notification()
            logger.info(f"用户选择: {user_choice}")

            if user_choice == "later":
                # 稍后提醒（10分钟）
                snooze_minutes = 10
                self.next_alert_time = time.time() + snooze_minutes * 60
                logger.info(f"用户选择稍后提醒，延迟 {snooze_minutes} 分钟")
                self.title_item.title = f"久坐提醒：{snooze_minutes} 分后再提醒"
                self.is_detecting = False
                return
            elif user_choice == "skip":
                # 跳过本次
                self.stats = Stats.add_ignored(self.stats)
                Stats.save(self.stats)
                self._reset_countdown()
                return

            # 用户点了「我知道了」：等待后再确认
            logger.info(f"用户点击我知道了，等待 {CONFIRM_DELAY_SECONDS} 秒后确认")
            self.title_item.title = f"久坐提醒：{CONFIRM_DELAY_SECONDS} 秒后确认…"
            time.sleep(CONFIRM_DELAY_SECONDS)

            self.title_item.title = "久坐提醒：确认检测中…"
            still_present = self._detect_person()
            logger.info(f"确认检测结果: {'仍有人' if still_present else '已离开'}")

            if still_present:
                # 还有人，再次提醒
                logger.info("确认仍有人，再次提醒")
                self.stats = Stats.add_ignored(self.stats)
                Stats.save(self.stats)
                self._run_detection_cycle()
            else:
                # 人走了，重置倒计时
                logger.info("确认已离开，重置倒计时")
                self.stats = Stats.add_activity(self.stats)
                Stats.save(self.stats)
                self._reset_countdown()
                
        except Exception as e:
            logger.error(f"检测周期出错: {e}", exc_info=True)
            rumps.notification(
                title="检测出错",
                subtitle="检测过程中出现错误",
                message=f"详细日志: {LOG_FILE}"
            )
            self._reset_countdown()

    def _reset_countdown(self):
        """重置倒计时（可以在任何线程中调用）"""
        self.next_alert_time = time.time() + self.config["interval_seconds"]
        logger.info(f"重置倒计时，下次检测时间: {datetime.fromtimestamp(self.next_alert_time).strftime('%Y-%m-%d %H:%M:%S')}")
        self.title_item.title = f"久坐提醒：重新开始倒计时"
        self.is_detecting = False

    # ------------------------------------------------------------------ #
    #  摄像头检测（单次，连拍多帧取多数）
    # ------------------------------------------------------------------ #
    def _detect_person(self) -> bool:
        """
        打开摄像头，连拍 CONFIRM_FRAMES 帧，
        超过半数帧检测到人脸则返回 True，否则返回 False。
        """
        logger.info("开始摄像头检测")
        cap = None
        
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                logger.error("无法打开摄像头")
                rumps.notification(
                    title="摄像头访问失败",
                    subtitle="无法打开摄像头",
                    message="请检查「系统设置 > 隐私与安全性 > 摄像头」中是否已授权"
                )
                return False

            # 预热：丢弃前几帧（部分摄像头冷启动时画面偏暗）
            logger.info("摄像头预热中...")
            for i in range(3):
                ret = cap.read()
                if not ret[0]:
                    logger.warning(f"预热帧 {i+1} 读取失败")

            detected_count = 0
            logger.info(f"开始连拍 {CONFIRM_FRAMES} 帧进行检测")
            
            for frame_idx in range(CONFIRM_FRAMES):
                ret, frame = cap.read()
                if not ret:
                    logger.warning(f"第 {frame_idx+1} 帧读取失败")
                    break
                    
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )
                
                if len(faces) > 0:
                    detected_count += 1
                    logger.info(f"第 {frame_idx+1} 帧: 检测到 {len(faces)} 个人脸")
                else:
                    logger.info(f"第 {frame_idx+1} 帧: 未检测到人脸")
                    
                time.sleep(0.1)

            result = detected_count > CONFIRM_FRAMES // 2
            logger.info(f"检测完成: {detected_count}/{CONFIRM_FRAMES} 帧检测到人脸，结果: {'有人' if result else '无人'}")
            return result
            
        except Exception as e:
            logger.error(f"摄像头检测过程出错: {e}", exc_info=True)
            rumps.notification(
                title="检测出错",
                subtitle="摄像头检测过程中出现错误",
                message=f"详细日志: {LOG_FILE}"
            )
            return False
            
        finally:
            if cap is not None:
                cap.release()
                logger.info("摄像头已释放")

    # ------------------------------------------------------------------ #
    #  提醒弹窗（优化版 - 更友好的选项）
    # ------------------------------------------------------------------ #
    def send_reminder_notification(self):
        """发送友好的提醒通知"""
        logger.info("发送提醒通知")
        
        # 使用 AppleScript 创建更友好的对话框
        applescript = '''
        try
            set dialogResult to display dialog "检测到您已久坐 ⏰\\n\\n建议起来活动一下，保护颈椎和眼睛～" buttons {"跳过本次", "10分钟后提醒", "我知道了"} default button "我知道了" with title "久坐提醒" with icon note
            set buttonReturned to button returned of dialogResult
            return buttonReturned
        on error
            return "我知道了"
        end try
        '''

        try:
            output = subprocess.check_output(
                ['osascript', '-e', applescript],
                stderr=subprocess.PIPE
            ).decode('utf-8').strip()
            
            logger.info(f"用户选择: {output}")
            
            if output == "10分钟后提醒":
                return "later"
            elif output == "跳过本次":
                return "skip"
            else:
                return "ok"
                    
        except subprocess.CalledProcessError as e:
            logger.error(f"AppleScript 执行失败: {e}", exc_info=True)
            rumps.notification(
                title="提醒弹窗失败",
                subtitle="无法显示提醒对话框",
                message=f"详细日志: {LOG_FILE}"
            )
        except Exception as e:
            logger.error(f"发送提醒时出错: {e}", exc_info=True)

        return "ok"


if __name__ == "__main__":
    try:
        logger.info("程序启动")
        reminder_app = SedentaryReminderApp()
        reminder_app.run()
    except Exception as e:
        logger.error(f"程序崩溃: {e}", exc_info=True)
        try:
            rumps.alert(
                title="程序崩溃",
                message=f"程序遇到严重错误:\n{str(e)}\n\n详细日志: {LOG_FILE}",
                ok="确定"
            )
        except:
            pass
        raise
