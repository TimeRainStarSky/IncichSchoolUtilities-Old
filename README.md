## 紫橙班牌实用工具 v3-Beta

**2021.03.08 注: 本项目仅是我学习研究(瞎折腾)过程中留下的部分代码, 感谢@lyc8503提供的源码**
**本项目基于：https://github.com/lyc8503/IncichSchoolUtilities 进行二次开发**


#### 部署

找一台服务器（我选择用手机Termux～(￣▽￣～)~）, 直接在 incich_school_utilities 目录下运行 `python3 main.py`. (初次运行需要根据提示配置.)

依赖: 

- 相关 python 库(在 pip 上都有)
- 查看服务器信息 screenfetch
（这个命令感觉不太好用，如果你有更好的查看方法请告诉我这个菜鸟，谢谢(๑>؂<๑））
- 网易云音乐需要 ffmpeg 用于调整音量（等待加入）

#### 基础功能: 

- 获取所有学校的邀请码: 直接运行 python get_code.py
- 班牌端指令互动(在班牌上向新增的家长发送 help 获取更多信息)
- 在班牌上听网易云音乐
- 在班牌上使用百度百科搜索
- **[New]** 在班牌上查看服务器文件
~~- **[TODO]** 在班牌上使用 Microsoft Todo~~
~~- **[TODO]** 在班牌上发送 QQ 消息~~

#### 进阶功能:

- 提供了 python 包装的 api, 在 /incich_school_utilities/incich_api 下, 有能力的人可以自行开发.



很抱歉 README 写的不是很详细, 但是代码都开源了. ~~自己看一下就会用了吧 :P~~（有一说一，确实(๑>؂<๑））
