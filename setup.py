from setuptools import setup

setup(
    name='PeterAnalyzer',
    version='1.0.0',
    packages=['peter_analyzer', 'peter_analyzer.data_set_creator'],
    url='',
    license='GPL-3.0',
    author='David Oberacker',
    author_email='david.oberacker@gmail.com',
    description='Analysis tool for Peter output files.',
    long_description=open('README.md').read(),
    install_requires=[
        "matplotlib >= 2.2.0",
        "DateTime >= 4.2",
        "coloredlogs"
    ],
    scripts=['src/peter_csv_analyzer.py'],
    package_dir={'peter_analyzer': 'src/peter_analyzer'},
)
