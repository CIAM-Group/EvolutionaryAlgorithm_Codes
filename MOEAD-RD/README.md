# MOEAD-RD
Li, H., Li, G., Jiang, Q., Wang, J., & Wang, Z. (2024). MOEA/D with customized replacement neighborhood and dynamic resource allocation for solving 3L-SDHVRP. Swarm and Evolutionary Computation, 101463. https://doi.org/10.1016/j.swevo.2023.101463

## Run

```shell
mkdir EvolutionaryAlgorithm_Codes && cd EvolutionaryAlgorithm_Codes
git init
git remote add origin https://github.com/CIAM-Group/EvolutionaryAlgorithm_Codes.git
git config core.sparseCheckout true
echo "MOEAD-RD/*" > .git/info/sparse-checkout
git pull origin main
cd MOEAD-RD/

python run.py
```
