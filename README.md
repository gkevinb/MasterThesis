# Master Thesis

## Data-Based Generation of Reliability Models

Aim: Design and implementation of methods for automated derivation of reliability models from data (e.g. A fault tree).

Objectives: Design a reliability model to produce streams of data. Analyze data for patterns using
artificial intelligence and/or machine learning. Derive and reproduce the reliability model from the data.
Compare the original reliability model and reproduced reliability model and evaluate the method of automated derivation.

[Download Thesis Report](https://gaborkevinbarta.com/files/GaborKevinBarta_MSc_Thesis.pdf)


## Installation

Use python 3.12 to run the application.

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Run analysis

```bash
python analysisFT.py
```

## Run analysis

```bash
python analysisFT.py
```


## Run proxel simulation

```bash
python proxel_example.py
```



## Dockerized app

Build container

```bash
docker build -t fault-tree-analysis .
```

Run container

```bash
docker run -it --rm fault-tree-analysis
```

Using docker desktop you can inspect generated files such as the time series data, truth table, and the graphs in png format in the container.
