# Extreme Summarization of Scientific Documents

The goal of this project is to reproduce the results of SciTLDR generation by stepwise utilizing extractive and abstractive methods and fine-tuning pre-trained models such as PacSum, BART on the SciTLDR dataset. Questions are as follows:

- Prepare the SciTLDR data for the listed models.

- Run the PacSum model on the SciTLDR.

- Fine-tune the BART model on the SciTLDR.

## Project structure:

- In the directory `/code`, you may get look into fine-tuned models (PacSum, BART).
- In the directory `/project-report`, you will find the report with a comparative analysis of the results obtained and the benchmarks from the SciTLDR article.

Information about the models' details, including instructions for the models fine-tuning, testing, we have stated in a separated `readme.md` files inside each subdirectory. Additionally, take a look at the report, where the experiment implementation are discussed in detail.
