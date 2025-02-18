# LifeChoice

This repository contains the code for testing different LLMs' role-playing capabilities in making life choices for literary characters.

## Data Availability

Due to copyright restrictions, we can only provide the Expert-written Descriptions method mentioned in our paper. Other methods require users to obtain the original books for experimentation.

For detailed data inquiries, please contact: rxu24@m.fudan.edu.cn

## Usage

1. Install the required dependencies
2. Set up your API keys for the LLMs you want to test
3. Run the tests using:

```bash
python test_llms.py --models gpt35 gpt4 claude gemini
```

You can specify which models to test by providing their names as arguments. Available options are: gpt35, gpt4, claude, gemini.

**Note**: Due to potential data contamination, model versions may affect the final results. Please verify and document the specific versions of the models you use.

## Citation

If you use this code/data in your research, please cite our paper:

```bibtex
@article{xu2024character,
  title={Character is Destiny: Can Large Language Models Simulate Persona-Driven Decisions in Role-Playing?},
  author={Xu, Rui and Wang, Xintao and Chen, Jiangjie and Yuan, Siyu and Yuan, Xinfeng and Liang, Jiaqing and Chen, Zulong and Dong, Xiaoqing and Xiao, Yanghua},
  journal={arXiv preprint arXiv:2404.12138},
  year={2024}
}
```