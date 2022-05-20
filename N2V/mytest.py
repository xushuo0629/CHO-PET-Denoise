


\$ python main.py --mode train \\
                 --scope [scope name] \\
                 --name_data [data name] \\
                 --dir_data [data directory] \\
                 --dir_log [log directory] \\
                 --dir_checkpoint [checkpoint directory]
                 --gpu_ids [gpu id; '-1': no gpu, '0, 1, ..., N-1': gpus]


python main.py --mode train --name_data pet  --dir_data ./datasets  --dir_log ./log  --dir_checkpoint ./checkpoints  --dir_result ./results --gpu_ids 0 --num_epoch  100 --batch_size 2
python main.py --mode train --name_data pet  --dir_data ./datasets  --dir_log ./log  --dir_checkpoint ./checkpoints --dir_result  ./results --gpu_ids 0 --num_epoch 1 --batch_size 2 --scope unet

tensorboard --logdir ./log/denoising_resnet\pet --port 6006

\$ python main.py --mode test \\
                 --scope resnet \\
                 --name_data bsd500 \\
                 --dir_data ./datasets \\
                 --dir_log ./log \\
                 --dir_checkpoint ./checkpoints \\
                 --dir_result ./results
                 --gpu_ids 0


python main.py --mode test --name_data pet  --dir_data ./datasets  --dir_log ./log  --dir_checkpoint ./checkpoints  --dir_result ./results3 --gpu_ids 0  --ny_in 320  --nx_in 320
results_timeM

python main.py --mode test --name_data petT  --dir_data ./datasets  --dir_log ./log  --dir_checkpoint ./checkpoints  --dir_result ./results_timeM --gpu_ids 0  --ny_in 320  --nx_in 320


//
python main.py --mode train --name_data petT  --dir_data ./datasets  --dir_log ./log  --dir_checkpoint ./checkpoints --dir_result  ./results --gpu_ids 0 --num_epoch 1 --batch_size 20 --scope unet --num_freq_save 1
python main.py --mode test --name_data petT  --dir_data ./datasets  --dir_log ./log  --dir_checkpoint ./checkpoints  --dir_result ./results_timeM --gpu_ids 0  --ny_in 320  --nx_in 320 --scope unet