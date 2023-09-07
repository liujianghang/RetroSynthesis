# RetroSynthesis
# 生物分子逆合成平台

这是一个为生物合成爱好者提供的生物分子逆合成平台。以下是平台的组件和文件下载链接：

- RetroSynthesis-back: 后端服务
- RetroSynthesis-front: 前端交互页面
- RetroSynthesis-model: 模型接口

你需要在 [这里的链接](https://drive.google.com/drive/folders/1HhsCmIERcquY6XCg18DhMbncdKpl0AA_?usp=drive_link) 下载相应的数据集，并将其放置在RetroSynthesis-model的 `app/retro/utils/data` 目录下。

同时，你还需要在 [这里的链接](https://drive.google.com/drive/folders/1SK7f6B3EfpHW-Hk2KF-EsPcyIYBmCAA6?usp=drive_link) 下载模型，并将其放置在RetroSynthesis-model的 `app/retro/utils/model` 目录下。

你需要配置 Node，并在控制台使用 `npm install` 命令安装前端所需的依赖包。

同时，后端和模型所需的环境配置分别在 `pom.xml` 和 `requirements.txt` 文件中，请确保你已正确设置环境。

此外，你还需要安装 MySQL 和 Redis在你的项目中。
