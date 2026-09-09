"""个人主页的唯一人工维护内容源。

运行 ``python portfolio.py validate|build|preview|clean``。
"""

from pathlib import Path
import sys

from portfolio_content import Portfolio


portfolio = Portfolio(
    site_name=dict(
        zh="郭瀚丞 个人主页",
        en="Hancheng Guo Homepage",
    ),
    author=dict(
        zh="郭瀚丞",
        en="Hancheng Guo",
    ),
    copyright_text=dict(
        zh="由 [_Lain-Ego0.github.io_](https://github.com/Lain-Ego0/Lain-Ego0.github.io) 提供支持",
        en="Powered by [_Lain-Ego0.github.io_](https://github.com/Lain-Ego0/Lain-Ego0.github.io)",
    ),
    last_update_date="2026-09-07",
    # favicon="assets/images/Avatar.jpg",
)


# region Profile

portfolio.set_profile(
    avatar="assets/images/Avatar.jpg",
    hero_background="assets/images/Portfolio-01-3.png",
    name=dict(
        zh="郭瀚丞",
        en="Hancheng Guo",
    ),
    summary=dict(
        zh=(
            "机器人开发爱好者，大三在读，目前于人形机器人公司实习。专注于 MCU 与 Linux 开发、运动控制、强化学习和机器人感知。"
        ),
        en=(
            "Robot development enthusiast and junior-year student. Interning at a humanoid robot company, "
            "with a focus on MCU and Linux development, motion control, reinforcement learning, "
            "and robot perception."
        ),
    ),
    email="hc.guo.tect@gmail.com",
)

portfolio.set_resume(
    label=dict(
        zh="下载简历",
        en="Download CV",
    ),
    url=dict(
        zh="assets/documents/简历测试.pdf",
        en="assets/documents/CVTest.pdf",
    ),
)

portfolio.add_contact(
    label=dict(
        zh="代码仓库",
        en="GitHub",
    ),
    icon="github",
    url="https://github.com/Hancheng-Guo",
)

portfolio.add_contact(
    label=dict(
        zh="ORCID 学术档案",
        en="ORCID",
    ),
    icon="orcid",
    url="https://orcid.org/0009-0005-2213-1604",
)

# endregion


# region Project

project_1 = portfolio.add_project(
    title=dict(
        zh="全国大学生机器人大赛 ROBOCON 足式机器人赛题",
        en="ROBOCON 2025 Quadruped Robot Challenge",
    ),
    date="2025-04",
    summary=dict(
        zh=(
            "2025赛季ROBOCON足式机器人全栈研发。负责从类植保无人机碳管装配工艺机械建模、"
            "力控制算法到3D雷达建图自主导航技术。带领团队在全国180余支队伍中取得竞速赛第30名、"
            "障碍赛第31名、越野赛34名的优异成绩。"
        ),
        en=(
            "Full-stack R&D for 2025 ROBOCON. Responsible for carbon tube assembly mechanical modeling, "
            "force control algorithms, and 3D LiDAR SLAM navigation. Led the team to achieve 30th in Speed, "
            "31st in Obstacle, and 34th in Cross-country among 180+ teams."
        ),
    ),
    thumbnail="assets/images/Portfolio-01.png",
    tags=(
        dict(
            zh="运动控制",
            en="Motion Control",
        ),
        dict(
            zh="SLAM",
            en="SLAM",
        ),
        dict(
            zh="机械设计",
            en="Mechanical Design",
        ),
        dict(
            zh="激光雷达",
            en="LiDAR",
        ),
    ),
)

page_1 = project_1.add_page(
    template="minimal",
)
page_1.add_image(
    "assets/images/Portfolio-01.png",
    alt=dict(
        zh="ROBOCON 足式机器人项目主图",
        en="ROBOCON quadruped robot project overview",
    ),
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "作为我真正入门强化学习控制的第一个项目，我选择了四足机器狗这个相对成熟的课题。"
            "\n"
            "机器狗有相当多的开源项目可以借鉴，因此可能有人会选择下载下来，跑通它，修改一下其中的内容，"
            "并包装成自己的项目，但我不想这样——因为学习不到一些被忽略的关键部分。"
            "\n"
            "在过往的科研经历中，我深知理解全流程的重要性，所以我选择基于 Stable-Baseline3 与 Mujoco 库，"
            "自己搭建机器狗的 RL 训练流程。"
        ),
        en=(
            "Full-stack R&D for 2025 ROBOCON. Responsible for carbon tube assembly mechanical modeling, "
            "force control algorithms, and 3D LiDAR SLAM navigation. Led the team to achieve 30th in Speed, "
            "31st in Obstacle, and 34th in Cross-country among 180+ teams."
        ),
    ),
)
page_1.add_heading(
    text=dict(
        zh="如何跑得更快？课程学习与奖励塑型",
        en="How Can It Run Faster? Curriculum Learning and Reward Shaping",
    ),
    level=3,
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "ROBOCON 作为机器人领域的顶尖赛事，对机械可靠性、电控稳定性、视觉准确性提出了较高的要求。"
            "\n"
            "在 2025 赛季我基本完整负责了足式机器人一队从机械建模、运动控制到自主导航的全栈研发，"
            "采用类植保无人机碳管装配工艺机构、力控制算法与 3D 雷达建图导航技术，取得 2025 年"
            "ROBOCON（江阴）足式机器人竞速赛全国 30 名、障碍赛全国 31 名、越野赛全国 34 名，"
            "共三项国二。"
        ),
        en=(
            "During the 2025 season, I worked across mechanical modeling, motion control, and autonomous "
            "navigation. The robot combined a carbon-tube structure, force-control algorithms, "
            "and 3D LiDAR mapping, earning three National Second Prizes."
        ),
    ),
)
page_1.add_heading(
    text=dict(
        zh="测试标题",
        en="Heading Test",
    ),
    level=4,
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "测试文本。"
        ),
        en=(
            "Test Text."
        ),
    ),
)
page_1.add_heading(
    text=dict(
        zh="测试标题",
        en="Heading Test",
    ),
    level=5,
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "测试文本。"
        ),
        en=(
            "Test Text."
        ),
    ),
)
page_1.add_image(
    "assets/images/Portfolio-01-3.png",
    alt=dict(
        zh="四足机器人训练与测试画面",
        en="Quadruped robot training and testing",
    ),
)
page_1.add_image(
    "assets/images/Portfolio-01-1.png",
    alt=dict(
        zh="四足机器人项目结构细节",
        en="Quadruped robot project structure detail",
    ),
)
page_1.add_image(
    "assets/images/Portfolio-01-2.png",
    alt=dict(
        zh="四足机器人项目运行结果",
        en="Quadruped robot project result",
    ),
)
page_1.add_github_link(
    url="https://github.com/Lain-Ego0/BRS-Parallel-Robot",
    label=dict(
        en="**Source code**",
        zh="**项目源码**"
    ),
)
page_1.add_doc_link(
    url="https://wcn9j5638vrr.feishu.cn/wiki/space/7570988375279517715?ccm_open_type=lark_wiki_spaceLink&open_tab_from=wiki_home",
    label=dict(
        en="**Docs**",
        zh="**技术文档**"
    ),
)
page_1.add_bilibili_link(
    url="https://www.bilibili.com/video/BV15wu4zuEmf",
    label=dict(
        en="**Demo**",
        zh="**演示视频**"
    ),
)


project_2 = portfolio.add_project(
    title=dict(
        zh="仿生波士顿大龙虾民用潜航机器人",
        en="Bionic Boston Lobster Submersible",
    ),
    summary=dict(
        zh=(
            "浮力可控多自由度龙虾水下机器人。负责控制系统开发（步进蠕动泵、电机/舵机驱动、"
            "陀螺仪融合、IIC编码器闭环），设计异形多旋翼矢量推进模型实现全向移动。"
            "硬件方面负责驱动选型与防水设计。获福建省大学生智能海洋装备大赛特等奖。"
        ),
        en=(
            "Buoyancy-controllable multi-DOF underwater robot. Developed control system (stepper pumps, "
            "motor/servo drive, gyro fusion, IIC encoder loop) and vector propulsion model for omnidirectional "
            "movement. Handled hardware selection and waterproofing. Won Special Prize in Fujian Intelligent "
            "Marine Equipment Competition."
        ),
    ),
    thumbnail="assets/images/Portfolio-02.png",
    tags=(
        dict(
            zh="嵌入式系统",
            en="Embedded Systems",
        ),
        dict(
            zh="矢量推进",
            en="Vector Propulsion",
        ),
        dict(
            zh="硬件设计",
            en="Hardware Design",
        ),
        dict(
            zh="防水设计",
            en="Waterproofing",
        ),
    ),
)
page_2 = project_2.add_page(
    template="minimal",
)
page_2.add_image(
    "assets/images/Portfolio-02.png",
    alt=dict(
        zh="仿生波士顿大龙虾潜航机器人整体展示",
        en="Bionic Boston lobster submersible overview",
    ),
)
page_2.add_paragraph(
    text=dict(
        zh=(
            "本项目为浮力可控的多自由度龙虾水下机器人。"
            "\n"
            "软件部分负责控制系统开发，设计了一套集成步进蠕动泵、电机与舵机驱动、陀螺仪数据处理以及"
            "读取 IIC 编码器闭环控制 360 度舵机的下位机框架，同时设计异形多旋翼的矢量推进模型，"
            "完善全向移动功能。在硬件设计部分负责了驱动器选型、降压电路以及防水设计等工作。"
            "\n"
            "作品获 2024 年福建省大学生智能海洋装备设计制作大赛水下机器人赛道特等奖，同时进一步代表"
            "福建理工大学参展 2024 世界航海装备大会，获得新华社、光明日报等媒体报道。"
        ),
        en=(
            "This project features a buoyancy-controllable multi-DOF lobster underwater robot."
            "\n"
            "On the software side, I was responsible for control system development, integrating stepper "
            "peristaltic pumps, motor and servo drives, gyroscope processing, and IIC encoder feedback for "
            "closed-loop control. I also designed a vector propulsion model for omnidirectional movement. "
            "On the hardware side, I handled driver selection, step-down circuit design, and waterproofing."
            "\n"
            "The project won the Special Prize in the 2024 Fujian University Student Intelligent Marine "
            "Equipment Design Competition and represented Fujian University of Technology at the "
            "2024 World Maritime Equipment Conference."
        ),
    ),
)
page_2.add_image(
    "assets/images/Portfolio-02-1.png",
    alt=dict(
        zh="潜航机器人机械结构细节",
        en="Submersible mechanical structure detail",
    ),
)
page_2.add_image(
    "assets/images/Portfolio-02-2.png",
    alt=dict(
        zh="潜航机器人控制系统展示",
        en="Submersible control system",
    ),
)
page_2.add_image(
    "assets/images/Portfolio-02-3.png",
    alt=dict(
        zh="潜航机器人比赛与展览成果",
        en="Submersible competition and exhibition result",
    ),
)


project_3 = portfolio.add_project(
    title=dict(
        zh="智能插秧收获一体机器人",
        en="Intelligent Planting and Harvesting Robot",
    ),
    summary=dict(
        zh=(
            "基于FreeRTOS的智能插秧收获农业机器人。通过控制DJI3508电机完成夹爪抬升与全向底盘控制，"
            "定位精度±5mm。参与气路设计与硬件布线，支持双机器人协同作业。"
        ),
        en=(
            "Smart planting and harvesting robot based on FreeRTOS. Controlled DJI3508 motors for gripper "
            "lifting and omni-directional chassis with ±5mm positioning accuracy. Participated in pneumatic "
            "design and hardware wiring, supporting dual-robot synergy."
        ),
    ),
    thumbnail="assets/images/Portfolio-03.png",
    tags=(
        dict(
            zh="FreeRTOS",
            en="FreeRTOS",
        ),
        dict(
            zh="电机控制",
            en="Motor Control",
        ),
        dict(
            zh="多机器人协同",
            en="Multi-robot Collaboration",
        ),
    ),
)
page_3 = project_3.add_page(
    template="minimal",
)
page_3.add_image(
    "assets/images/Portfolio-03.png",
    alt=dict(
        zh="智能插秧收获一体机器人比赛现场",
        en="Intelligent planting and harvesting robot at the competition",
    ),
)
page_3.add_paragraph(
    text=dict(
        zh=(
            "基于 FreeRTOS 实时操作系统，进行智能插秧与收获一体化农业机器人控制系统编写。"
            "\n"
            "通过控制 DJI3508 电机，完成夹爪抬升机构、全向轮底盘、全向定位系统等模块的功能调试，"
            "使夹爪动作定位精度控制在 ±5 mm 内；同步参与气路系统设计与硬件布线工作，"
            "支持与另一台自主运行机器人协同作业，高效完成任务。"
        ),
        en=(
            "Based on FreeRTOS, I developed the control system for an integrated intelligent planting and "
            "harvesting agricultural robot. By controlling DJI3508 motors, I completed the gripper lifting, "
            "omnidirectional chassis, and positioning functions with ±5 mm accuracy. I also participated in "
            "pneumatic system design and hardware wiring for collaborative dual-robot operation."
        ),
    ),
)
page_3.add_github_link(
    url="https://github.com/Lain-Ego0/ROBOCON2024-R1",
)
page_3.add_bilibili_link(
    url="https://www.bilibili.com/video/BV1VH4y1A7aM/",
)

# endregion


# region Publication

portfolio.add_publication(
    publication_type="journal",
    title="[_RapidPD: Rapid Human and Pet Presence Detection System for Smart Vehicles via Wi-Fi_](https://ieeexplore.ieee.org/document/10971911)",
    venue=(
        '**H. Guo**, Z. Chen, M. Huang and X. Y. Zhang, '
        '"RapidPD: Rapid Human and Pet Presence Detection System for Smart Vehicles via Wi-Fi," '
        'in *IEEE Transactions on Aerospace and Electronic Systems*, '
        'vol. 61, no. 4, pp. 10459-10470, Aug. 2025, doi: 10.1109/TAES.2025.3562838.'
    ),
)

portfolio.add_publication(
    publication_type="conference",
    title="[_Children Presence Detection System in Vehicles via Wi-Fi Devices_](https://ieeexplore.ieee.org/abstract/document/11310443)",
    venue=(
        'Z. Chen, **H. Guo** and X. Zhang, '
        '"Children Presence Detection System in Vehicles via Wi-Fi Devices," '
        '*2025 IEEE 102nd Vehicular Technology Conference (VTC2025-Fall)*, Chengdu, China, '
        '2025, pp. 1-5, doi: 10.1109/VTC2025-Fall65116.2025.11310443.'
    ),
)

portfolio.add_publication(
    publication_type="conference",
    title="[_A WiPD-DL Network for in-Vehicle Secure Channel Detection_](https://ieeexplore.ieee.org/abstract/document/11352220)",
    venue=(
        'Z. Chen, **H. Guo**, J. Wen and X. Y. Zhang, '
        '"A WiPD-DL Network for in-Vehicle Secure Channel Detection," '
        '*2025 Seventeenth International Conference on Wireless Communications and Signal Processing (WCSP)*, Chongqing, China, '
        '2025, pp. 1-6, doi: 10.1109/WCSP68525.2025.1010649.'
    ),
)

# endregion


# region Timeline

portfolio.add_timeline_event(
    date="2024-05",
    title=dict(
        zh="开源 SliverWolf 桌面四足",
        en="Open Source SliverWolf Desktop Quadruped",
    ),
    description=dict(
        zh=(
            "发布具备语音控制与机械臂协同作业能力的桌面级串联四足机器人 SliverWolf。"
        ),
        en=(
            "Released SliverWolf, a desktop serial quadruped with voice control and robotic-arm collaboration."
        ),
    ),
)
portfolio.add_timeline_event(
    date="2024-07",
    title=dict(
        zh="2024 ROBOCON 全国赛",
        en="2024 ROBOCON National Competition",
    ),
    description=dict(
        zh=(
            "基于 FreeRTOS 完成 R1 机器人嵌入式控制系统开发，实现 ±5 mm 定位精度、球体发射和夹爪夹取功能。"
        ),
        en=(
            "Developed the FreeRTOS embedded control system for the R1 robot,\n"
            "achieving ±5 mm positioning accuracy, ball launching, and gripper functions."
        ),
    ),
)
portfolio.add_timeline_event(
    date="2024-08",
    title=dict(
        zh="2024 福建省大学生电子设计大赛",
        en="2024 Fujian Undergraduate Electronics Design Contest",
    ),
    description=dict(
        zh=(
            "基于 MSPM0G3507 开发自动驾驶小车系统并进入省级测试阶段。"
        ),
        en=(
            "Developed an MSPM0G3507-based autonomous vehicle system and qualified for provincial testing."
        ),
    ),
)
portfolio.add_timeline_event(
    date="2024-11",
    title=dict(
        zh="福建省大学生智能海洋装备设计制作大赛",
        en="Fujian Intelligent Marine Equipment Design Competition",
    ),
    description=dict(
        zh=(
            "负责浮力可控多自由度龙虾水下机器人的控制系统开发，获特等奖。"
        ),
        en=(
            "Led control-system development for a buoyancy-controlled multi-DOF lobster robot, winning the Special Prize."
        ),
    ),
)
portfolio.add_timeline_event(
    date="2024-12",
    title=dict(
        zh="2024 世界航海装备大会",
        en="2024 World Marine Equipment Conference",
    ),
    description=dict(
        zh=(
            "代表福建理工大学参展并展示仿生波士顿大龙虾机器人，获新华社等媒体报道。"
        ),
        en=(
            "Represented Fujian University of Technology and exhibited the bionic Boston lobster robot, "
            "receiving national media coverage."
        ),
    ),
)
portfolio.add_timeline_event(
    date="2025-07",
    title=dict(
        zh="2025 ROBOCON 全国赛",
        en="2025 ROBOCON National Competition",
    ),
    description=dict(
        zh=(
            "负责足式机器人全栈研发，在竞速、障碍和越野赛中获得三项国家二等奖。"
        ),
        en=(
            "Led full-stack development of the quadruped robot and earned three National Second Prizes."
        ),
    ),
)
portfolio.add_timeline_event(
    date="2025-08",
    title=dict(
        zh="2025 全国大学生电子设计大赛",
        en="2025 National Undergraduate Electronics Design Contest",
    ),
    description=dict(
        zh=(
            "负责自动测距系统功率计的硬件设计与制作，获全国二等奖。"
        ),
        en=(
            "Designed and fabricated the power-meter hardware for an automatic ranging system, winning the National Second Prize."
        ),
    ),
)
portfolio.add_timeline_event(
    date="2025-09",
    title=dict(
        zh="开源 BRS 并联四足机器人",
        en="Open Source BRS Parallel Quadruped Robot",
    ),
    description=dict(
        zh=(
            "在 GitHub 开源 BRS 并联四足机器人的机械结构与控制代码。"
        ),
        en=(
            "Open-sourced the mechanical structure and control code of the BRS parallel quadruped robot on GitHub."
        ),
    ),
)
portfolio.add_timeline_event(
    date=dict(
        start="2025-10",
        end="2026-03",
    ),
    title=dict(
        zh="高擎机电实习",
        en="Internship at Gaoqing Electromechanical",
    ),
    description=dict(
        zh=(
            "负责 HTDW4438 仿生四足机器人的机械设计、控制算法开发与系统集成测试。"
        ),
        en=(
            "Responsible for mechanical design, control-algorithm development,\n"
            "and system-integration testing for the HTDW4438 bionic quadruped robot."
        ),
    ),
)
portfolio.add_timeline_event(
    date=dict(
        start="2026-09"
    ),
    title=dict(
        zh="测试时间线",
        en="Timeline Test",
    ),
    description=dict(
        zh=(
            "- 第一行\n"
            "- 第二行"
        ),
        en=(
            "- Line 1\n"
            "- Line 2"
        ),
    ),
)

# endregion


# region Education

portfolio.add_education(
    date=dict(
        start="2022-09",
        end="2026-06",
    ),
    position=dict(
        zh="测试学科 学士",
        en="Bachelor of Test",
    ),
    institute=dict(
        zh="测试学校",
        en="University of Test",
    ),
    location=dict(
        zh="中国北京",
        en="China",
    ),
    detail=dict(
        zh="测试文案",
        en="Test",
    ),
)

# endregion


# region Work Experience

portfolio.add_work_experience(
    date=dict(
        start="2025-10",
    ),
    position=dict(
        zh="测试实习",
        en="Test of Intern",
    ),
    company=dict(
        zh="测试公司",
        en="Test of Company",
    ),
    location=dict(
        zh="中国芜湖",
        en="China",
    ),
    detail=dict(
        zh=(
            "- 第一行\n"
            "- 第二行"
        ),
        en=(
            "- Line 1\n"
            "- Line 2"
        ),
    ),
)

# endregion


# region Skill

portfolio.add_tech_group(
    title=dict(
        zh="嵌入式开发",
        en="Embedded",
    ),
    items=[
        dict(
            name=dict(
                zh="STM32",
                en="STM32",
            ),
        ),
        dict(
            name=dict(
                zh="ESP32",
                en="ESP32",
            ),
        ),
        dict(
            name=dict(
                zh="FreeRTOS",
                en="FreeRTOS",
            ),
        ),
        dict(
            name=dict(
                zh="C/C++",
                en="C/C++",
            ),
        ),
    ],
)
portfolio.add_tech_group(
    title=dict(
        zh="机器人技术",
        en="Robotics",
    ),
    items=[
        dict(
            name=dict(
                zh="ROS/ROS2",
                en="ROS/ROS2",
            ),
        ),
        dict(
            name=dict(
                zh="Gazebo",
                en="Gazebo",
            ),
        ),
        dict(
            name=dict(
                zh="运动控制",
                en="Motion Control",
            ),
        ),
        dict(
            name=dict(
                zh="强化学习",
                en="Reinforcement Learning",
            ),
        ),
    ],
)
portfolio.add_tech_group(
    title=dict(
        zh="硬件设计",
        en="Hardware",
    ),
    items=[
        dict(
            name=dict(
                zh="Altium",
                en="Altium",
            ),
        ),
        dict(
            name=dict(
                zh="SolidWorks",
                en="SolidWorks",
            ),
        ),
        dict(
            name=dict(
                zh="PCB",
                en="PCB",
            ),
        ),
    ],
)
portfolio.add_tech_group(
    title=dict(
        zh="软件与工具",
        en="Software",
    ),
    items=[
        dict(
            name=dict(
                zh="Linux",
                en="Linux",
            ),
        ),
        dict(
            name=dict(
                zh="Python",
                en="Python",
            ),
        ),
        dict(
            name=dict(
                zh="Git",
                en="Git",
            ),
        ),
    ],
)

# endregion


# region Award

portfolio.add_award(
    date="2025-08",
    title=dict(
        zh="Award Test",
        en="Award Test",
    ),
    status="test",
)

# endregion


if __name__ == "__main__":
    from portfolio_content.cli import main

    if len(sys.argv) > 1 and sys.argv[1] in {"validate", "build", "preview"}:
        sys.argv.insert(2, str(Path(__file__).resolve()))
    raise SystemExit(main())
