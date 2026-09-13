"""个人主页的唯一人工维护内容源。

运行 ``python portfolio.py validate|build|preview|clean``。
"""

from pathlib import Path
import sys

from portfolio_content import Portfolio


portfolio = Portfolio(
    site_name=dict(zh="郭瀚丞 | 个人主页", en="Hancheng Guo | Homepage"),
    author=dict(zh="郭瀚丞", en="Hancheng Guo"),
    copyright_text=dict(
        zh="由 [_Lain-Ego0.github.io_](https://github.com/Lain-Ego0/Lain-Ego0.github.io) 提供支持",
        en="Powered by [_Lain-Ego0.github.io_](https://github.com/Lain-Ego0/Lain-Ego0.github.io)",
    ),
    last_update_date="2026-09-13",
    favicon="assets/icons/favicon.svg",
)

# Page sections are configured here. Profile is always present first; the
# remaining entries choose both what is shown and its order on each page.
portfolio.set_home_field(("projects", "publications", "timeline"))
# portfolio.set_cv_field(("education", "work experience", "publications", "tech stack", "awards and scholarships"))
portfolio.set_cv_field(("education", "publications", "tech stack", "awards and scholarships"))


# region Profile

portfolio.set_profile(
    name=dict(zh="郭瀚丞", en="Hancheng Guo"),
    summary=dict(
        zh=(
            # "正在寻找机器人方向的博士研究机会。"
            "研究兴趣包括机器人学习、强化学习与足式机器人，"
            "尤其关注学习驱动的运动控制与决策，使机器人能够在复杂环境中实现稳健、自主的行为。"
            "此前的研究聚焦无线感知."
        ),
        en=(
            # "Seeking PhD opportunities in robotics. "
            "My research interests include Robot Learning, Reinforcement Learning, "
            "and Legged Robotics, with a focus on learning-based locomotion and decision-making "
            "for robust, autonomous behavior in complex environments. "
            "My previous research focused on wireless sensing."
        ),
    ),
    avatar="assets/images/Avatar.jpg",
    hero_background="assets/images/Portfolio-01-3.png",
    email="hc.guo.tect@gmail.com",
)

portfolio.set_resume(
    url=dict(
        zh="assets/documents/简历测试.pdf",
        en="assets/documents/CVTest.pdf",
    ),
)

portfolio.add_contact(
    label=dict(zh="代码仓库", en="GitHub"),
    icon="assets/icons/github.svg",
    url="https://github.com/Hancheng-Guo",
)
portfolio.add_contact(
    label=dict(zh="ORCID 学术档案", en="ORCID"),
    icon="assets/icons/orcid.svg",
    url="https://orcid.org/0009-0005-2213-1604",
)

# endregion


# region Project RapidPD

project_1 = portfolio.add_project(
    title=dict(
        zh="低成本无线感知：从物理建模到真实验证",
        en="Low-Cost Wireless Sensing: From Modeling to Real-World Validation",
    ),
    date="2025-08",
    summary=dict(
        zh=(
            "负责商用 Wi-Fi 车内感知系统的软件算法与系统调试，并通过四个月的真实车辆实验完成验证。"
            "成果以第一作者发表于 IEEE TAES，并受邀在 WOCC 2025 作专题报告。"
        ),
        en=(
            "Developed and debugged the software algorithm for a commercial-Wi-Fi in-vehicle sensing system, "
            "then validated it through four months of real-world vehicle tests. "
            "First-author IEEE TAES paper and WOCC 2025 invited talk."
        ),
    ),
    thumbnail="assets/images/projects/rapidpd/RapidPD-WOCC2025-talk.jpg",
    tags=(
        dict(zh="无线感知", en="Wireless Sensing"),
        dict(zh="信号处理", en="Signal Process"),
        dict(zh="真实场景验证", en="Real-World Validation"),
    ),
)

page_1 = project_1.add_page(template="minimal")
page_1.add_paragraph(
    text=dict(
        zh=(
            "RapidPD 是一个利用车辆现有 Wi-Fi 设备检测遗留儿童与宠物的低成本感知系统。"
            "我在项目中负责软件算法设计与系统调试：从安全需求和响应延迟出发建立感知模型，"
            "将算法接入商用硬件的数据链路，并通过长期真实场景实验不断定位和修正问题。"
        ),
        en=(
            "RapidPD is a low-cost sensing system that reuses existing in-vehicle Wi-Fi devices to detect a child or pet "
            "left behind. My responsibility was software algorithm design and system debugging: I translated the safety "
            "and latency requirements into a sensing model, integrated the algorithm with the commercial-hardware data "
            "pipeline, and used long-term field tests to locate and correct failures."
        ),
    ),
)
page_1.add_heading(
    text=dict(
        zh="从约束到可运行算法",
        en="From Constraints to a Working Algorithm",
    ),
    level=3,
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "真正的难点是同时满足低成本、全车覆盖与快速响应。已有方法依赖较长时间序列来等待微弱运动累积，"
            "我没有继续堆叠模型复杂度，而是回到传播机制本身：微小运动会以结构化方式影响同一时刻的多个子载波。"
            "这个观察把“等待更久”改写为“利用横向结构”，最终将检测窗口缩短到 1 秒。"
            "对我而言，这个决策体现的是一种可迁移的问题求解方式：先寻找限制性能的根因，再选择与根因匹配的表示和算法。"
        ),
        en=(
            "The hard part was meeting low cost, full-cabin coverage, and fast response at the same time. Existing methods "
            "waited for weak motion to accumulate over long sequences. Instead of adding model complexity, I returned to "
            "the propagation mechanism and recognized that small motion leaves structure across many subcarriers at the "
            "same instant. That reframed the task from 'wait longer' to 'use the horizontal structure' and reduced the "
            "detection window to one second. The transferable lesson is to identify the root bottleneck before choosing the representation and algorithm."
        ),
    ),
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "硬件平台由团队提供，我的工作从数据进入软件之后开始。我把物理假设拆成可逐步检查的处理流程，"
            "围绕硬件漂移、复杂多径和弱运动信号反复调试，在真实采集数据中定位误差来源，"
            "并通过归一化、特征增强与判决平滑提高稳定性。最终算法只需 20 Hz 采样和 1 秒数据即可完成判断，"
            "在实车测试中达到 99.05% 总体准确率与 99.32% 真阳性率。"
        ),
        en=(
            "The hardware platform was provided by the team; my work began once its data entered the software pipeline. "
            "I decomposed the physical hypothesis into processing stages that could be inspected independently, then "
            "debugged against hardware drift, complex multipath, and weak motion in real measurements. Normalization, "
            "feature enhancement, and decision smoothing emerged from those observed failure modes. The final algorithm "
            "operates on 20 Hz sampling and one second of data, reaching 99.05% overall accuracy and 99.32% true positive rate in vehicle tests."
        ),
    ),
)
page_1.add_heading(
    text=dict(
        zh="用真实场景寻找失效边界",
        en="Finding Failure Boundaries in the Real World",
    ),
    level=3,
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "我没有把高准确率当作终点，而是把实验设计成对系统假设的压力测试。"
            "四个多月的采集覆盖 10 个不同体型的人与宠物、11 个车内位置，以及停车楼、路边、露天区域和高架桥下等环境。"
            "我同时设置传统基线与模块消融，检查性能提升究竟来自核心思路还是实验偶然性。"
            "这套验证思路与机器人真实部署相同：关心的不是平均分数，而是系统在位置变化、弱信号和环境迁移下何时失效。"
        ),
        en=(
            "I treated evaluation as a stress test of the system's assumptions, not a search for one high score. More than "
            "four months of collection covered ten people and pets of different sizes, eleven cabin positions, and parking "
            "structures, roadsides, open areas, and an elevated bridge. I also compared against a conventional baseline and "
            "ablated key modules to separate genuine improvement from experimental coincidence. This mirrors real robotics "
            "deployment: the important question is when a system fails under viewpoint, signal-strength, and environment shifts."
        ),
    ),
)
page_1.add_image(
    "assets/images/projects/rapidpd/RapidPD-experiment.jpg",
    alt=dict(
        zh="真实环境下的测试结果展示",
        en="Presentation of test results in real-world conditions",
    ),
    caption=dict(
        zh="真实环境下的测试结果展示",
        en="Presentation of test results in real-world conditions",
    ),
)
page_1.add_heading(
    text=dict(
        zh="研究成果与技术表达",
        en="Research Outcome and Technical Communication",
    ),
    level=3,
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "该工作以第一作者发表于 *IEEE Transactions on Aerospace and Electronic Systems*。"
            "随后我受邀在 WOCC 2025 作 30 分钟专题报告，将长期项目压缩成一条清晰的论证链："
            "为什么问题重要、现有方法为何受限、关键洞察是什么、系统是否真的在复杂环境中成立。"
            "能够完成研究是一种能力，能够让不同背景的研究者快速理解并质疑它，是另一种能力。"
        ),
        en=(
            "The work was published with me as first author in *IEEE Transactions on Aerospace and Electronic Systems*. "
            "I was then invited to give a 30-minute talk at WOCC 2025, compressing a long project into a clear argument: "
            "why the problem matters, why prior approaches are constrained, what the key insight is, and whether the system "
            "actually holds up in complex environments. Completing the research is one skill; making it quickly understandable "
            "and open to critique by researchers from other backgrounds is another."
        ),
    ),
)
page_1.add_paper_link(url="https://ieeexplore.ieee.org/document/10971911")
page_1.add_image(
    "assets/images/projects/rapidpd/RapidPD-WOCC2025-program.jpg",
    alt=dict(
        zh="WOCC 2025 议程中的受邀报告条目",
        en="The invited-talk listing in the WOCC 2025 program",
    ),
    caption=dict(
        zh="WOCC 2025 官方议程中的 Invited Speech 时段（16:20-16:50）",
        en="The RapidPD invited-speech slot in the WOCC 2025 program (16:20-16:50)",
    ),
)
page_1.add_image(
    "assets/images/projects/rapidpd/RapidPD-WOCC2025-talk-wide.jpg",
    alt=dict(
        zh="郭瀚丞在 WOCC 2025 作 RapidPD 受邀报告",
        en="Hancheng Guo presenting the RapidPD invited talk at WOCC 2025",
    ),
    caption=dict(
        zh="在 WOCC 2025 作受邀报告",
        en="Presenting the invited talk at WOCC 2025",
    ),
)
page_1.add_paragraph(
    text=dict(
        zh=(
            "这项工作训练的是一种通用的，能够应用到各领域的底层能力：从模糊需求中定义可验证问题，"
            "把物理直觉转化为算法，把算法接入真实硬件，并用跨场景实验寻找系统的失效边界。"
        ),
        en=(
            "This work developed the general and basic abilities, which can be applied across various fields: "
            "defining a testable problem from an ambiguous need, translating physical intuition into an algorithm, "
            "integrating that algorithm with real hardware, "
            "and using cross-scenario experiments to locate failure boundaries. "
        ),
    ),
)

# endregion


# region Project RosLittleRound

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
        zh="测试项目",
        en="Test Project",
    ),
    summary=dict(
        zh=(
            "测试项目概述\n"
            "测试项目概述\n"
            "测试项目概述\n"
            "测试项目概述"
        ),
        en=(
            "Summary of Test Project.\n"
            "Summary of Test Project.\n"
            "Summary of Test Project.\n"
            "Summary of Test Project"
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


project_4 = portfolio.add_project(
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
page_4 = project_4.add_page(
    template="minimal",
)
page_4.add_image(
    "assets/images/Portfolio-03.png",
    alt=dict(
        zh="智能插秧收获一体机器人比赛现场",
        en="Intelligent planting and harvesting robot at the competition",
    ),
)
page_4.add_paragraph(
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
page_4.add_github_link(
    url="https://github.com/Lain-Ego0/ROBOCON2024-R1",
)
page_4.add_bilibili_link(
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
        zh="发布具备语音控制与机械臂协同作业能力的桌面级串联四足机器人 SliverWolf。",
        en="Released SliverWolf, a desktop serial quadruped with voice control and robotic-arm collaboration.",
    ),
)

# endregion


# region Education

portfolio.add_education(
    date=dict(start="2023-09", end="2026-06"),
    position=dict(zh="电子信息 硕士", en="Master of Electronic Information"),
    institute=dict(zh="华南理工大学", en="South China University of Technology"),
    location=dict(zh="中国广州", en="China"),
    detail=dict(
        zh=(
            "- 发表论文：SCI 一区一作论文 1篇，国际会议论文 2篇\n"
            "- 竞赛获奖：中国研究生电子设计竞赛全国二等奖"
        ),
        en=(
            "- Publications: 1 first-author Q1 journal paper and 2 international conference papers\n"
            "- Award: National Finals Second Prize in a nationwide graduate-level electronics design competition"
        ),
    ),
)

portfolio.add_education(
    date=dict(start="2019-09", end="2023-06"),
    position=dict(zh="信息工程 学士", en="Bachelor of Information Engineering"),
    institute=dict(zh="华南理工大学", en="South China University of Technology"),
    location=dict(zh="中国广州", en="China"),
    detail=dict(
        zh="- GPA: 3.83/4.0, 专业前 10%",
        en="- GPA: 3.83/4.0, top 10% of graduates",
    ),
)

# endregion


# region Skill

portfolio.add_tech_group(
    title=dict(zh="编程与开发", en="Programming"),
    items=[
        dict(name="Python"),
        dict(name="C++"),
        dict(name="ROS2"),

        dict(name="PyTorch"),
        dict(name="MATLAB"),
        dict(name="Git"),
    ],
)
portfolio.add_tech_group(
    title=dict(zh="机器人技术", en="Robotics"),
    items=[
        dict(name=dict(zh="强化学习", en="Reinforcement Learning")),
        dict(name=dict(zh="课程学习", en="Curriculum")),

        dict(name="MuJoCo"),
        dict(name="Isaac Lab"),
    ],
)

# endregion


# region Award

portfolio.add_award(
    title=dict(
        zh="汇顶科技一等奖学金",
        en="Goodix Technology First-Class Scholarship",
    ),
    description=dict(
        zh="表彰在学业与科研方面的杰出表现",
        en="Recognition for outstanding performance of academic and research",
    ),
)

portfolio.add_award(
    title=dict(
        zh="第十八届中国研究生电子设计竞赛全国总决赛二等奖、华为专项奖二等奖",
        en=(
            "National Second Prize and Huawei Special Award Second Prize, "
            "18th China Postgraduate Electronics Design Contest"
        ),
    ),
    description=dict(
        zh="专项赛道全国第七名",
        en="Ranked 7th nationally in the Special Track",
    ),
)

portfolio.add_award(
    title=dict(
        zh="中国科协 2021 青少年高校科学营优秀志愿者",
        en="Outstanding Volunteer, 2021 Youth University Science Camp, China Association for Sience and Technology",
    ),
    description=dict(
        zh="体现公共服务意识与组织协作能力",
        en="Demonstrating commitment to public service and organizational collaboration",
    ),
)

# endregion


if __name__ == "__main__":
    from portfolio_content.cli import main

    if len(sys.argv) > 1 and sys.argv[1] in {"validate", "build", "preview"}:
        sys.argv.insert(2, str(Path(__file__).resolve()))
    raise SystemExit(main())
