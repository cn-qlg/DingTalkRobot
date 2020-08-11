import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dingtalk_push_robot",
    version="0.0.1",
    author="cn_qlg",
    author_email="cn_qlg@163.com",
    description="A wrapper for dingtalk push robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cn-qlg/DingTalkRobot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
