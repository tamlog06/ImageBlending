 #sh main.sh /workspace/images /workspace/output

dataroot=${1}
output_dir=${2}

shadowimage_path=${output_dir}'/harmonized'
shadowfree_path=${output_dir}'/harmonized'
mask_path=${dataroot}'/foreground_object_mask'
instance_path=${dataroot}'/foreground_object_mask'
bg_shadow_path=${dataroot}'/background_shadow_mask'
bg_shadow_bin_path=${dataroot}'/background_shadow_mask_bin'
bg_instance_path=${dataroot}'/background_object_mask'
shadowed_path=${output_dir}'/shadowed'
harmonized_path=${output_dir}'/harmonized'
result_path=${output_dir}'/result'


# 0. Binalize the mask
echo "Binalize mask"
python3 binary.py -i ${bg_shadow_path} -o ${bg_shadow_bin_path}
bg_shadow_path=${bg_shadow_bin_path}

# 1. Image Harmonization via Harmonizer
echo "Image Harmonization"
cd Harmonizer
python3 -m demo.image_harmonization.run --input-path ${dataroot} --output-path ${harmonized_path}


# 2. Shadow Removal via ShadowRemover
cd ../Object-Shadow-Generation-Dataset-DESOBA/src/script/

batchs=1
GPU=0
lr=0.0002
loadSize=256
fineSize=256
L1=100
model=SGRNet
G='RESNEXT18'
ngf=32


L_shadowrecons=10
L_imagerecons=10
L_GAN=0.1

#####network design
DISPLAY_PORT=8002
D='pixel'
lr_D=0.0002


#####datset selected
# datasetmode=shadowparam
datasetmode=ShadowGenerationDatasetInference


checkpoint='../../TrainedModels/SGRNet_TrainedModel'



model_name=SelfAttention
NAME="${model_name}_G${G}_C${ngf}_D${D}_lrD${lr_D}"


OTHER="--no_crop --no_flip --no_rotate --serial_batches"

CMD="python3 ../generate.py --loadSize ${loadSize} \
    --phase test --eval
    --name ${NAME} \
    --checkpoints_dir ${checkpoint} \
    --epoch latest\
    --fineSize $fineSize --model $model\
    --batch_size $batchs --display_port ${DISPLAY_PORT}
    --display_server http://localhost
    --gpu_ids ${GPU} --lr ${lr} \
    --dataset_mode $datasetmode\
    --mask_train $mask_path\
    --norm instance\
    --dataroot  ${dataroot}\
    --instance_path $instance_path\
    --shadowimg_path $shadowimage_path\
    --shadowmask_path $mask_path\
    --shadowfree_path $shadowfree_path\
    --bg_shadow_path $bg_shadow_path\
    --bg_instance_path $bg_instance_path\
    --lambda_M1 $L_shadowrecons --lambda_I1 $L_imagerecons --lambda_GAN $L_GAN 
    --netG $G\
    --ngf $ngf
    --netD $D
    --lr_D $lr_D
    --output_dir $shadowed_path
    --use

    $OTHER"

echo $CMD
eval $CMD

# 3. upscale shadowed image by poisson image editing
cd ../../../poisson-image-editing
python3 main.py ${shadowed_path} ${harmonized_path} ${result_path} mix
