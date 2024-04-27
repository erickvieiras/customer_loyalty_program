data=$date
path='/home/erickvieira/Documentos/repos/clustering_project'
path_to_envs='/home/erickvieira/.pyenv/versions/3.11.7/envs/clusteringvenv/bin/'
$path_to_envs/papermill $path/src/deploy.ipynb $path/reports/deploy_$data.ipynb
