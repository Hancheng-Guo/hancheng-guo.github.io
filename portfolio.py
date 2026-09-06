"""当前个人主页的唯一项目内容源。

运行 ``python portfolio.py validate|build|preview|clean``。完整说明见
docs/PYTHON_GUIDE.md。网页读取本文件生成的 assets/data/projects.json。
"""

from pathlib import Path
import sys

from portfolio_content import Portfolio


portfolio = Portfolio()


# Project 1: ROBOCON 2025 Quadruped Robot Challenge
project_1 = portfolio.add_project(
    title={"en": "ROBOCON 2025 Quadruped Robot Challenge", "zh": "全国大学生机器人大赛ROBOCON足式机器人赛题"},
    summary={
        "en": "Full-stack R&D for 2025 ROBOCON. Responsible for carbon tube assembly mechanical modeling, force control algorithms, and 3D LiDAR SLAM navigation. Led the team to achieve 30th in Speed, 31st in Obstacle, and 34th in Cross-country among 180+ teams.",
        "zh": "2025赛季ROBOCON足式机器人全栈研发。负责从类植保无人机碳管装配工艺机械建模、力控制算法到3D雷达建图自主导航技术。带领团队在全国180余支队伍中取得竞速赛第30名、障碍赛第31名、越野赛34名的优异成绩。",
    },
    thumbnail="assets/images/Portfolio-01.png",
    tags=("Motion Control", "SLAM", "Mechanical Design", "LiDAR"),
)
page_1 = project_1.add_page(template="minimal")
page_1.add_image("assets/images/Portfolio-01.png", alt={"en": "ROBOCON quadruped robot project overview", "zh": "ROBOCON 足式机器人项目主图"})
page_1.add_paragraph({
    "en": "Full-stack R&D for 2025 ROBOCON. Responsible for carbon tube assembly mechanical modeling, force control algorithms, and 3D LiDAR SLAM navigation. Led the team to achieve 30th in Speed, 31st in Obstacle, and 34th in Cross-country among 180+ teams.",
    "zh": "作为我真正入门强化学习控制的第一个项目，我选择了四足机器狗这个相对成熟的课题。\n\n机器狗有相当多的开源项目可以借鉴，因此可能有人会选择下载下来，跑通它，修改一下其中的内容，并包装成自己的项目，但我不想这样——因为学习不到一些被忽略的关键部分。\n\n在过往的科研经历中，我深知理解全流程的重要性，所以我选择基于 Stable-Baseline3 与 Mujoco 库，自己搭建机器狗的 RL 训练流程。",
})
page_1.add_heading("如何跑得更快？课程学习与奖励塑型", level=3, languages=("zh",))
page_1.add_paragraph(
    "ROBOCON 作为机器人领域的顶尖赛事，对机械可靠性、电控稳定性、视觉准确性提出了较高的要求。\n\n在 2025 赛季我基本完整负责了足式机器人一队从机械建模、运动控制到自主导航的全栈研发，采用类植保无人机碳管装配工艺机构、力控制算法与 3D 雷达建图导航技术，取得 2025 年 ROBOCON（江阴）足式机器人竞速赛全国 30 名、障碍赛全国 31 名、越野赛全国 34 名（全国赛参赛队伍 180 余支），共三项国二。",
    languages=("zh",),
)
page_1.add_image(
    "assets/images/Portfolio-01-3.png",
    alt={"en": "Quadruped robot training and testing", "zh": "四足机器人训练与测试画面"},
)
page_1.add_image(
    "assets/images/Portfolio-01-1.png",
    alt={"en": "Quadruped robot project structure detail", "zh": "四足机器人项目结构细节"},
)
page_1.add_image(
    "assets/images/Portfolio-01-2.png",
    alt={"en": "Quadruped robot project result", "zh": "四足机器人项目运行结果"},
)
page_1.add_link("github", "https://github.com/Lain-Ego0/BRS-Parallel-Robot")
page_1.add_link("techDoc", "https://wcn9j5638vrr.feishu.cn/wiki/space/7570988375279517715?ccm_open_type=lark_wiki_spaceLink&open_tab_from=wiki_home")
page_1.add_link("demo", "https://www.bilibili.com/video/BV15wu4zuEmf")


# Project 2: Bionic Boston Lobster Submersible
project_2 = portfolio.add_project(
    title={"en": "Bionic Boston Lobster Submersible", "zh": "仿生波士顿大龙虾民用潜航机器人"},
    summary={
        "en": "Buoyancy-controllable multi-DOF underwater robot. Developed control system (stepper pumps, motor/servo drive, gyro fusion, IIC encoder loop) and vector propulsion model for omnidirectional movement. Handled hardware selection and waterproofing. Won Special Prize in Fujian Intelligent Marine Equipment Competition.",
        "zh": "浮力可控多自由度龙虾水下机器人。负责控制系统开发（步进蠕动泵、电机/舵机驱动、陀螺仪融合、IIC编码器闭环），设计异形多旋翼矢量推进模型实现全向移动。硬件方面负责驱动选型与防水设计。获福建省大学生智能海洋装备大赛特等奖。",
    },
    thumbnail="assets/images/Portfolio-02.png",
    tags=("Embedded Systems", "Vector Propulsion", "Hardware Design", "Waterproofing"),
)
page_2 = project_2.add_page(template="minimal")
page_2.add_image("assets/images/Portfolio-02.png", alt={"en": "Bionic Boston lobster submersible overview", "zh": "仿生波士顿大龙虾潜航机器人整体展示"})
page_2.add_paragraph({
    "en": "This project features a buoyancy-controllable multi-DOF lobster underwater robot.\n\nOn the software side, I was responsible for the control system development, designing a lower-level machine framework that integrates stepper peristaltic pumps, motor and servo drives, gyroscope data processing, and IIC encoder feedback for closed-loop control of 360-degree servos. I also designed a vector propulsion model for the irregular multi-rotor structure to achieve omnidirectional movement. On the hardware side, I handled driver selection, step-down circuit design, and waterproofing.\n\nThe project won the Special Prize in the Underwater Robot Track at the 2024 Fujian University Student Intelligent Marine Equipment Design Competition. It also represented Fujian University of Technology at the 2024 World Maritime Equipment Conference, receiving coverage from media outlets such as Xinhua News Agency and Guangming Daily.",
    "zh": "本项目为浮力可控的多自由度龙虾水下机器人。\n\n软件部分负责控制系统开发，设计了一套集成步进蠕动泵、电机与舵机驱动、陀螺仪数据处理以及读取 IIC 编码器闭环控制 360 度舵机的下位机框架，同时设计异形多旋翼的矢量推进模型，完善全向移动功能。在硬件设计部分负责了驱动器选型、降压电路以及防水设计等工作。\n\n作品获 2024 年福建省大学生智能海洋装备设计制作大赛水下机器人赛道特等奖，同时进一步代表福建理工大学参展 2024 世界航海装备大会，获得新华社、光明日报等媒体报道。",
})
page_2.add_image(
    "assets/images/Portfolio-02-1.png",
    alt={"en": "Submersible mechanical structure detail", "zh": "潜航机器人机械结构细节"},
)
page_2.add_image(
    "assets/images/Portfolio-02-2.png",
    alt={"en": "Submersible control system", "zh": "潜航机器人控制系统展示"},
)
page_2.add_image(
    "assets/images/Portfolio-02-3.png",
    alt={"en": "Submersible competition and exhibition result", "zh": "潜航机器人比赛与展览成果"},
)
page_2.add_link("github", None)
page_2.add_link("techDoc", None)
page_2.add_link("demo", None)


# Project 3: Intelligent Planting and Harvesting Robot
project_3 = portfolio.add_project(
    title={"en": "Intelligent Planting and Harvesting Robot", "zh": "智能插秧收获一体机器人"},
    summary={
        "en": "Smart planting & harvesting robot based on FreeRTOS. Controlled DJI3508 motors for gripper lifting and omni-directional chassis with ±5mm positioning accuracy. Participated in pneumatic design and hardware wiring, supporting dual-robot synergy.",
        "zh": "基于FreeRTOS的智能插秧收获农业机器人。通过控制DJI3508电机完成夹爪抬升与全向底盘控制，定位精度±5mm。参与气路设计与硬件布线，支持双机器人协同作业。",
    },
    thumbnail="assets/images/Portfolio-03.png",
    tags=("FreeRTOS", "Motor Control", "Multi-robot Synergy"),
)
page_3 = project_3.add_page(template="minimal")
page_3.add_image(
    "assets/images/Portfolio-03.png",
    alt={"en": "Intelligent planting and harvesting robot at the competition", "zh": "智能插秧收获一体机器人比赛现场"},
)
page_3.add_paragraph({
    "en": "Based on the FreeRTOS real-time operating system, I developed the control system for an integrated intelligent planting and harvesting agricultural robot.\n\nBy controlling DJI3508 motors, I completed the functional debugging of the gripper lifting mechanism, omnidirectional chassis, and omnidirectional positioning system, achieving a gripper positioning accuracy within ±5 mm. I also participated in the pneumatic system design and hardware wiring, supporting collaborative operation with another autonomous robot to efficiently complete tasks.",
    "zh": "基于 FreeRTOS 实时操作系统，进行智能插秧与收获一体化农业机器人控制系统编写。\n\n通过控制 DJI3508 电机，完成夹爪抬升机构、全向轮底盘、全向定位系统等模块的功能调试，使夹爪动作定位精度控制在 ±5 mm 内；同步参与气路系统设计与硬件布线工作，支持与另一台自主运行机器人协同作业，高效完成任务。",
})
page_3.add_link("github", "https://github.com/Lain-Ego0/ROBOCON2024-R1")
page_3.add_link("techDoc", None)
page_3.add_link("demo", "https://www.bilibili.com/video/BV1VH4y1A7aM/?spm_id_from=333.337.search-card.all.click&vd_source=193a56b6f00b33090010ba20d05cfef7")


# Timeline
portfolio.add_timeline_event(
    date="2024-05",
    title={"en": "Open Source SliverWolf Desktop Quadruped", "zh": "开源 SliverWolf 桌面四足"},
    description={"en": "Released SliverWolf, a desktop-level serial quadruped robot featuring voice control and robotic arm collaborative capabilities.", "zh": "发布 SliverWolf，一款具备语音控制与机械臂协同作业能力的桌面级串联四足机器人。"},
)
portfolio.add_timeline_event(
    date="2024-07",
    title={"en": "2024 ROBOCON National Competition", "zh": "2024ROBOCON全国赛"},
    description={"en": "Developed the embedded control system for the R1 robot based on FreeRTOS, achieving ±5mm positioning accuracy, ball launching, and gripper functionalities.", "zh": "基于FreeRTOS完成R1机器人嵌入式控制系统开发，实现±5mm定位精度，球体发射、夹爪夹取功能。"},
)
portfolio.add_timeline_event(
    date="2024-08",
    title={"en": "2024 Fujian Undergraduate Electronics Design Contest", "zh": "2024福建省大学生电子设计大赛"},
    description={"en": "Developed an autonomous driving car system based on the MSPM0G3507, qualifying for the provincial testing stage.", "zh": "基于MSPM0G3507开发自动驾驶小车系统，进入省测。"},
)
portfolio.add_timeline_event(
    date="2024-11",
    title={"en": "Fujian Intelligent Marine Equipment Design Competition", "zh": "福建省大学生智能海洋装备设计制作大赛"},
    description={"en": "Led the development of the control system for a buoyancy-controlled multi-DOF lobster underwater robot, winning the Grand Prize.", "zh": "负责开发浮力可控多自由度龙虾水下机器人的控制系统，获特等奖。"},
)
portfolio.add_timeline_event(
    date="2024-12",
    title={"en": "2024 World Marine Equipment Conference", "zh": "2024 世界航海装备大会"},
    description={"en": "Represented Fujian University of Technology as an exhibitor, showcasing the bionic Boston Lobster robot; covered by media outlets including Xinhua News Agency.", "zh": "代表福建理工大学参展，展示仿生波士顿大龙虾机器人，获新华社等媒体报道。"},
)
portfolio.add_timeline_event(
    date="2025-07",
    title={"en": "2025 ROBOCON National Competition", "zh": "2025 ROBOCON 全国赛"},
    description={"en": "Responsible for full-stack R&D of the legged robot. Ranked 30th nationally in the Sprint Race, 31st in the Obstacle Race, and 34th in the Cross-Country Race, securing three National Second Prizes.", "zh": "负责足式机器人全栈研发。获足式机器人竞速赛全国30名、障碍赛31名、越野赛34名，共三项国二佳绩。"},
)
portfolio.add_timeline_event(
    date="2025-08",
    title={"en": "2025 National Undergraduate Electronics Design Contest", "zh": "2025全国大学生电子设计大赛"},
    description={"en": "Responsible for the hardware design and fabrication of the power meter for an automatic ranging system, winning the National Second Prize.", "zh": "负责自动测距系统的功率计硬件设计与制作，获全国二等奖。"},
)
portfolio.add_timeline_event(
    date="2025-09",
    title={"en": "Open Source BRS Parallel Quadruped Robot", "zh": "开源 BRS 并联四足机器人"},
    description={"en": "Open-sourced the mechanical structure and control code of the BRS parallel quadruped robot on GitHub.", "zh": "在GitHub开源BRS并联四足机器人的机械结构与控制代码。"},
)
portfolio.add_timeline_event(
    date={"en": "2025-10 to 2026-03", "zh": "2025-10至2026-3"},
    title={"en": "Internship at Gaoqing Electromechanical", "zh": "高擎机电激情实习中"},
    description={"en": "Responsible for mechanical design, control algorithm development, and system integration testing for the HTDW4438 bionic quadruped robot (both open-source and commercial versions).", "zh": "负责HTDW4438仿生四足机器人的机械设计、控制算法开发与系统集成测试,分为开源版本与产品化版本"},
)


# Tech Stack
portfolio.add_tech_group(title={"en": "Embedded", "zh": "嵌入式开发"}, items=[
    {"name": "STM32", "icon": "fas fa-microchip"}, {"name": "ESP32", "icon": "fas fa-wifi"},
    {"name": "FreeRTOS", "icon": "fas fa-cogs"}, {"name": "C/C++", "icon": "fas fa-code"},
])
portfolio.add_tech_group(title={"en": "Robotics", "zh": "机器人技术"}, items=[
    {"name": "ROS/ROS2", "icon": "fas fa-robot"}, {"name": "Gazebo", "icon": "fas fa-cube"},
    {"name": "Motion Control", "icon": "fas fa-wave-square"}, {"name": "RL", "icon": "fas fa-brain"},
])
portfolio.add_tech_group(title={"en": "Hardware", "zh": "硬件设计"}, items=[
    {"name": "Altium", "icon": "fas fa-pencil-ruler"}, {"name": "SolidWorks", "icon": "fas fa-drafting-compass"},
    {"name": "PCB", "icon": "fas fa-layer-group"},
])
portfolio.add_tech_group(title={"en": "Software", "zh": "软件与工具"}, items=[
    {"name": "Linux", "icon": "fab fa-linux"}, {"name": "Python", "icon": "fab fa-python"},
    {"name": "Git", "icon": "fab fa-git-alt"},
])


# Let's Connect
portfolio.add_contact(label={"en": "Bilibili", "zh": "哔哩哔哩"}, icon="fab fa-bilibili", url="https://space.bilibili.com/385516781/upload/video")
portfolio.add_contact(label={"en": "GitHub", "zh": "代码仓库"}, icon="fab fa-github", url="https://github.com/Lain-Ego0")
portfolio.add_contact(label={"en": "Twitter", "zh": "推特"}, icon="fab fa-twitter", url="https://x.com/Lain_Ego0")
portfolio.add_contact(label={"en": "Zhihu", "zh": "知乎"}, icon="fab fa-zhihu", url="https://www.zhihu.com/people/hua-99-50-21")


if __name__ == "__main__":
    from portfolio_content.cli import main

    if len(sys.argv) > 1 and sys.argv[1] in {"validate", "build", "preview"}:
        sys.argv.insert(2, str(Path(__file__).resolve()))
    raise SystemExit(main())
