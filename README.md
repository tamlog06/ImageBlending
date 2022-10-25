# How to start

install docker, (ref)[https://qiita.com/gen10nal/items/1e7fe8a1b2e9ad1e7919] \\
clone this repo \\
then

`
cd ImageBlending \\
docker build -t torun . \\
docker run -it --rm --gpus all -v $(pwd):/workspace torun \\
sh main.sh [images directory] [output directory] \\
`

Notice that directory is specified as absolute path.
