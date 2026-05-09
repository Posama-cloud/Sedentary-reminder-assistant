#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 10秒倒计时版本
用于快速测试久坐提醒助手的功能
"""

import rumps
import cv2
import time
import os
import threading
import subprocess
import logging
from datetime import datetime

# --- 测试配置 ---
APP_ICON_PATH = "image_0.png"

# 测试模式：10秒倒计时
DEFAULT_INTERVAL_SECONDS = 10

# 确认延迟：5秒（测试用）
CONFIRM_DELAY_SECONDS = 5

# 检测帧数
CONFIRM_FRAMES = 5

# --- 日志配置 ---
LOG_DIR = os.path.expanduser("~/Library/Logs/久坐提醒助手")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "test.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SedentaryReminderApp(rumps.App):
    def __init__(self):
        logger.info("=" * 60)
        logger.info("久坐提醒助手启动 [测试模式 - 10秒倒计时]")
        logger.info("=" * 60)
        
        if os.path.exists(APP_ICON_PATH):
            super(SedentaryReminderApp, self).__init__("测试", icon=APP_ICON_PATH)
            logger.info(f"使用图标: {APP_ICON_PATH}")
        else:
            super(SedentaryReminderApp, self).__init__("测试")
            logger.warning(f"图标文件不存在: {APP_ICON_PATH}")

        self.title_item = rumps.MenuItem("测试模式：初始化中…", callback=None)
        self.menu = [
            "重置计时器", 
            "立即测试检测", 
            "查看日志", 
            "关于", 
            rumps.separator, 
            self.title_item
        ]

        self.next_alert_time = time.time() + DEFAULT_INTERVAL_SECONDS
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

        # 显示测试模式提示
        rumps.alert(
            title="测试模式启动",
            message=f"测试模式已启动！\n\n倒计时: {DEFAULT_INTERVAL_SECONDS} 秒\n确认延迟: {CONFIRM_DELAY_SECONDS} 秒\n\n日志位置: {LOG_FILE}",
            ok="开始测试"
        )

        # 使用 rumps.timer 启动定时器（在主线程中运行）
        self.timer = rumps.Timer(self.update_countdown, 1)
        self.timer.start()
        logger.info("初始化完成")

    @rumps.clicked("重置计时器")
    def reset_timer(self, _):
        logger.info("用户手动重置计时器")
        self.next_alert_time = time.time() + DEFAULT_INTERVAL_SECONDS
        self.title_item.title = "测试模式：已重置"

    @rumps.clicked("立即测试检测")
    def test_detection(self, _):
        logger.info("用户触发立即测试")
        self.title_item.title = "测试模式：检测中…"
        
        def run_test():
            try:
                person_present = self._detect_person()
                result = "检测到有人" if person_present else "未检测到人"
                logger.info(f"测试结果: {result}")
                
                rumps.notification(
                    title="检测测试结果",
                    subtitle=result,
                    message=f"详细日志请查看: {LOG_FILE}"
                )
                self.title_item.title = f"测试模式：{result}"
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
            title="久坐提醒助手 - 测试模式",
            message=f"测试模式配置:\n\n倒计时: {DEFAULT_INTERVAL_SECONDS} 秒\n确认延迟: {CONFIRM_DELAY_SECONDS} 秒\n检测帧数: {CONFIRM_FRAMES} 帧\n\n日志位置: {LOG_FILE}",
            ok="好的"
        )

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
                self._update_countdown_display(remaining)
            else:
                logger.info("倒计时结束，开始检测流程")
                self.is_detecting = True
                threading.Thread(target=self._run_detection_cycle, daemon=True).start()
                
        except Exception as e:
            logger.error(f"更新倒计时出错: {e}", exc_info=True)
            self.title_item.title = f"测试模式：出错了"

    def _update_countdown_display(self, remaining_seconds):
        remaining = int(remaining_seconds)
        self.title_item.title = f"测试模式：还有 {remaining} 秒"

    def _run_detection_cycle(self):
        logger.info("开始检测周期")
        self.title_item.title = "测试模式：检测中…"

        try:
            person_present = self._detect_person()
            logger.info(f"初次检测结果: {'有人' if person_present else '无人'}")

            if not person_present:
                logger.info("未检测到人，重置倒计时")
                self._reset_countdown()
                return

            logger.info("检测到有人，发送提醒")
            user_choice = self.send_interactive_reminder()
            logger.info(f"用户选择: {user_choice}")

            if user_choice["action"] == "snooze":
                snooze_minutes = user_choice["minutes"]
                self.next_alert_time = time.time() + snooze_minutes * 60
                logger.info(f"用户选择稍后提醒，延迟 {snooze_minutes} 分钟")
                self.title_item.title = f"测试模式：{int(snooze_minutes)} 分后提醒"
                self.is_detecting = False
                return

            logger.info(f"用户点击我知道了，等待 {CONFIRM_DELAY_SECONDS} 秒后确认")
            self.title_item.title = f"测试模式：{CONFIRM_DELAY_SECONDS} 秒后确认"
            time.sleep(CONFIRM_DELAY_SECONDS)

            self.title_item.title = "测试模式：确认检测中…"
            still_present = self._detect_person()
            logger.info(f"确认检测结果: {'仍有人' if still_present else '已离开'}")

            if still_present:
                logger.info("确认仍有人，再次提醒")
                self._run_detection_cycle()
            else:
                logger.info("确认已离开，重置倒计时")
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
        self.next_alert_time = time.time() + DEFAULT_INTERVAL_SECONDS
        logger.info(f"重置倒计时，下次检测时间: {datetime.fromtimestamp(self.next_alert_time).strftime('%Y-%m-%d %H:%M:%S')}")
        self.title_item.title = f"测试模式：重新倒计时"
        self.is_detecting = False

    def _detect_person(self) -> bool:
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

    def send_interactive_reminder(self):
        logger.info("发送交互式提醒")
        applescript = '''
        try
            set dialogResult to display dialog "【测试模式】检测到您已久坐，请起来活动一下！\\n\\n若现在不方便，请在下方输入推迟的分钟数，并点击「稍后提醒」：" default answer "0.5" buttons {"稍后提醒", "我知道了"} default button "我知道了" with title "久坐提醒助手 - 测试"
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
                            snooze_mins = 0.5
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
        logger.info("测试程序启动")
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
