# Illuminus Bot - Fine-tuned Qwen 3B Model

This repository contains the fine-tuned Qwen 3B model for **Illuminus Bot**, along with model checkpoints and necessary configurations for reproducing or deploying the model.

## Getting Started

### Cloning the Repository

Since this repository contains large files (model checkpoints and other related files) that are tracked using **Git Large File Storage (LFS)**, you will need to install Git LFS to successfully clone and work with these large files.

#### 1. Install Git LFS

To install Git LFS, follow the instructions below based on your operating system:

- **Windows/macOS/Linux:**

  Run the following command to install Git LFS:

  ```bash
  git lfs install
If you don't have Git installed, you can download and install it from here.

2. Clone the Repository
Once Git LFS is installed, you can clone the repository as usual, and Git LFS will automatically handle the large files:

bash
Copy code
git clone https://github.com/yourusername/illuminus_bot.git
Git LFS will fetch the large files (e.g., model checkpoints) after cloning.

Repository Structure
models/: Contains the model checkpoints and necessary files for loading the fine-tuned Qwen 3B model.
config/: Contains configuration files such as train_model_config.json for setting up the model training environment.
notebooks/: Includes Jupyter notebooks for training, testing, and running inference with the fine-tuned model.
Working with Large Files
If you make changes to the large files (e.g., model files, checkpoints), make sure that you commit and push them using Git LFS.

When adding new large files (larger than 50 MB), you need to track them with Git LFS by running:

bash
Copy code
git lfs track "*.pt"  # for PyTorch checkpoint files
git lfs track "*.bin"  # for model binary files
git lfs track "*.safetensors"  # for safetensors files
Then add the .gitattributes file and commit the changes:

bash
Copy code
git add .gitattributes
git commit -m "Track large files using Git LFS"
git push origin main
Usage
Once you have cloned the repository and installed the necessary dependencies, you can use the fine-tuned Qwen 3B model as described in the notebooks:

Load the model: Load the fine-tuned Qwen 3B model and tokenizer.
Inference: Run inference using the example notebooks provided in the notebooks/ directory.
Troubleshooting
If you encounter any issues related to cloning or working with large files, make sure:

Git LFS is installed and properly configured.

If you have already cloned the repository without Git LFS, you can install Git LFS and then fetch the large files with:

bash
Copy code
git lfs pull