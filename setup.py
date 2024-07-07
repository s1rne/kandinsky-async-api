from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='AsyncKandinsky',
    version='2.0.3',
    author='s1rne',
    author_email='s.simaranov8@gmail.com',
    description='This module is designed for asynchronous use of the kandinsky neural network and easy integration into your project.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/s1rne/kandinsky-async-api',
    packages=find_packages(),
    install_requires=['aiohttp>=3.8.4'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='kandinsky text2img async api',
    project_urls={
        'GitHub': 'https://github.com/s1rne/kandinsky-async-api'
    },
    python_requires='>=3.6'
)
