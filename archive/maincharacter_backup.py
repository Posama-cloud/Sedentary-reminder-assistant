import rumps
import cv2
import time
import os
import threading
import subprocess
import logging
from datetime import datetime

# --- 配置 ---
APP_ICON_PATH = "image_0.png"

# 正式间隔：3600 秒（1小时）；测试时可改为较小值（如 10）
DEFAULT_INTERVAL_SECONDS = 3600

# 点击「我知道了」后，等待多少秒再做第二次确认检测
CONFIRM_DELAY_SECONDS = 30

# 第二次确认时，连拍多少帧来判断是否有人（取多数结果，避免单帧误判）
CONFIRM_FRAMES = 5

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
        logging.StreamHandler()  # 同时输出到控制台
    ]
)
logger = logging.getLogger(__name__)


class SedentaryReminderApp(rumps.App):
    def __init__(self):
        logger.info("=" * 60)
        logger.info("久坐提醒助手启动")
        logger.info("=" * 60)
        
        if os.path.exists(APP_ICON_PATH):
            super(SedentaryReminderApp, self).__init__("", icon=APP_ICON_PATH)
            logger.info(f"使用图标: {APP_ICON_PATH}")
        else:
            super(SedentaryReminderApp, self).__init__("久坐")
            logger.warning(f"图标文件不存在: {APP_ICON_PATH}")

        self.title_item = rumps.MenuItem("久坐提醒：初始化中…", callback=None)
        self.menu = [
            "重置计时器", 
            "立即测试检测", 
            "查看日志", 
            "关于", 
            rumps.separator, 
            self.title_item
        ]

        # 下次触发提醒的目标时间戳
        self.next_alert_time = time.time() + DEFAULT_INTERVAL_SECONDS

        self.is_detecting = False  # 标记是否正在检测中

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

        # 使用 rumps.timer 启动定时器（在主线程中运行）
        self.timer = rumps.Timer(self.update_countdown, 1)
        self.timer.start()
        
        logger.info("初始化完成")

    # ------------------------------------------------------------------ #
    #  首次启动欢迎弹窗
    # ------------------------------------------------------------------ #
    def check_and_show_welcome(self):
        config_file = os.path.expanduser('~/.sedentary_reminder_config')
        if os.path.exists(config_file):
            logger.info("跳过欢迎提示（用户已选择不再显示）")
            return

        logger.info("显示欢迎提示")
        response = rumps.alert(
            title="启动成功",
            message=f"久坐提醒助手已在后台运行。\n\n程序将每隔一小时检测一次摄像头，若检测到您仍在座位上，将提醒您起来活动。\n\n日志位置: {LOG_FILE}",
            ok="我知道了",
            cancel="不再显示",
            icon_path=APP_ICON_PATH if os.path.exists(APP_ICON_PATH) else None
        )

        if response == 0:
            with open(config_file, 'w') as f:
                f.write("hide")
            logger.info("用户选择不再显示欢迎提示")

    # ------------------------------------------------------------------ #
    #  菜单栏操作
    # ------------------------------------------------------------------ #
    @rumps.clicked("重置计时器")
    def reset_timer(self, _):
        logger.info("用户手动重置计时器")
        self.next_alert_time = time.time() + DEFAULT_INTERVAL_SECONDS
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
            title="久坐提醒助手",
            message=f"一个通过摄像头检测您是否久坐的零成本工具。\n\n每隔一小时检测一次，有人则提醒活动，没人则自动重新计时。\n\n日志位置: {LOG_FILE}",
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
                self._reset_countdown()
                return

            # 有人，弹提醒
            logger.info("检测到有人，发送提醒")
            user_choice = self.send_interactive_reminder()
            logger.info(f"用户选择: {user_choice}")

            if user_choice["action"] == "snooze":
                # 稍后提醒：按用户指定分钟数延迟
                snooze_minutes = user_choice["minutes"]
                self.next_alert_time = time.time() + snooze_minutes * 60
                logger.info(f"用户选择稍后提醒，延迟 {snooze_minutes} 分钟")
                self.title_item.title = f"久坐提醒：{int(snooze_minutes)} 分后再提醒"
                self.is_detecting = False
                return

            # 用户点了「我知道了」：等待后再确认
            logger.info(f"用户点击我知道了，等待 {CONFIRM_DELAY_SECONDS} 秒后确认")
            self.title_item.title = f"久坐提醒：{CONFIRM_DELAY_SECONDS} 秒后确认…"
            time.sleep(CONFIRM_DELAY_SECONDS)

            self.title_item.title = "久坐提醒：确认检测中…"
            still_present = self._detect_person()
            logger.info(f"确认检测结果: {'仍有人' if still_present else '已离开'}")

            if still_present:
                # 还有人，再次提醒（递归调用）
                logger.info("确认仍有人，再次提醒")
                self._run_detection_cycle()
            else:
                # 人走了，重置倒计时
                logger.info("确认已离开，重置倒计时")
                self._reset_countdown()
                
        except Exception as e:
            logger.error(f"检测周期出错: {e}", exc_info=True)
            rumps.notification(
                title="检测出错",
                subtitle="检测过程中出现错误",
                message=f"详细日志: {LOG_FILE}"
            )
            # 出错后也重置倒计时，避免卡住
            self._reset_countdown()

    def _reset_countdown(self):
        """重置倒计时（可以在任何线程中调用）"""
        self.next_alert_time = time.time() + DEFAULT_INTERVAL_SECONDS
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
    #  提醒弹窗
    # ------------------------------------------------------------------ #
    def send_interactive_reminder(self):
        """调用 macOS 原生对话框提醒用户起来活动。"""
        logger.info("发送交互式提醒")
        applescript = '''
        try
            set dialogResult to display dialog "检测到您已久坐，请起来活动一下！\\n\\n若现在不方便，请在下方输入推迟的分钟数，并点击「稍后提醒」：" default answer "5" buttons {"稍后提醒", "我知道了"} default button "我知道了" with title "久坐提醒助手"
            return (button returned of dialogResult) & "|" & (text returned of dialogResult)
        on error
            return "取消|0"
        end try
        '''

        try:
            output = subprocess.check_output(
                ['osascript', '-e', applescript],
                stderr=subprocess.PIPE
            ).decode('utf-8').strip()
            
            logger.info(f"AppleScript 返回: {output}")

            if "|" in output:
                button, text_val = output.split("|", 1)
                if button == "稍后提醒":
                    try:
                        snooze_mins = float(text_val)
                        if snooze_mins <= 0:
                            snooze_mins = 1
                        logger.info(f"用户选择稍后提醒 {snooze_mins} 分钟")
                        return {"action": "snooze", "minutes": snooze_mins}
                    except ValueError as e:
                        logger.warning(f"解析推迟时间失败: {text_val}, 错误: {e}")
                        return {"action": "reset"}
                elif button == "我知道了":
                    logger.info("用户点击我知道了")
                    return {"action": "reset"}
                    
        except subprocess.CalledProcessError as e:
            logger.error(f"AppleScript 执行失败: {e}, stderr: {e.stderr.decode('utf-8') if e.stderr else 'N/A'}", exc_info=True)
            rumps.notification(
                title="提醒弹窗失败",
                subtitle="无法显示提醒对话框",
                message=f"详细日志: {LOG_FILE}"
            )
        except Exception as e:
            logger.error(f"发送提醒时出错: {e}", exc_info=True)

        return {"action": "reset"}


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
