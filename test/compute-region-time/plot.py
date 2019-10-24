
import os, sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.colors import hsv_to_rgb



label_fontsize = 16


fig, axes = plt.subplots(1, 1, figsize=(4, 3))

ax = axes

ds_list = range(0, 4)
acc_compute_time_uvm = []
acc_compute_time_uvm_err_set = [(39.069, 46.973), (38.67, 41.38), (41.4, 43.09), (43.51, 45.04)]
for a in acc_compute_time_uvm_err_set:
	acc_compute_time_uvm.append((a[0]+a[1])/2)
acc_compute_time_uvm_err = []
for a in zip(acc_compute_time_uvm, acc_compute_time_uvm_err_set):
	mean = a[0]
	b0 = a[1][0]
	b1 = a[1][1]
	acc_compute_time_uvm_err.append(max(mean-b0, b1-mean))

acc_compute_time_ach = []
acc_compute_time_ach_err_set = [(20.357, 20.893), (20.6, 21.43), (20.98, 23.48), (21.18, 21.9)]
for a in acc_compute_time_ach_err_set:
	acc_compute_time_ach.append((a[0]+a[1])/2)
acc_compute_time_ach_err = []
for a in zip(acc_compute_time_ach, acc_compute_time_ach_err_set):
	mean = a[0]
	b0 = a[1][0]
	b1 = a[1][1]
	acc_compute_time_ach_err.append(max(mean-b0, b1-mean))





ind = np.arange(len(ds_list))
width = 0.2


print acc_compute_time_ach[3]-acc_compute_time_uvm[3], "B"
print "%.2f%%" % (100.0*(acc_compute_time_ach[3]-acc_compute_time_uvm[3])/acc_compute_time_uvm[3])


# line = ax.plot(ds_list, acc_compute_time_uvm, "--x", label="UVM", color="#1f77b4")
rects1 = ax.bar(ind - width/2, acc_compute_time_uvm, width, yerr=acc_compute_time_uvm_err, edgecolor='k', color="white", label='UVM')

# line = ax.plot(ds_list, acc_compute_time_ach, "--^", label="pointerchain", color="#ff7f0c")
rects1 = ax.bar(ind + width/2, acc_compute_time_ach, width, yerr=acc_compute_time_ach_err, edgecolor='k', color="gray", label='pointerchain')



# line = ax.plot(ds_list, cuda_gflops['advVel'], "--v", label="CUDA-AdvanceVelocity", color='#2ca02c')
# print line[0].get_color()

# ax.plot(ds_list, acc_gflops['force'], "-x", label="ACC-ComputeForce")
# ax.plot(ds_list, acc_gflops['advPos'], "-^", label="ACC-AdvancePosition")
# ax.plot(ds_list, acc_gflops['advVel'], "-v", label="ACC-AdvanceVelocity")

# ax.set_yscale('log')

ax.set_xlabel('Level', fontsize=label_fontsize)
ax.set_ylabel('Device time (us)', fontsize=label_fontsize)

for tick in ax.yaxis.get_major_ticks():
	tick.label.set_fontsize(label_fontsize-2)



ax.set_xticks(ds_list)
ds_list_title = [format(_ss, ',') for _ss in ds_list]
ax.set_xticklabels(ds_list_title, fontsize=label_fontsize-2)

ax.set_yticks(range(0, 61, 10))

# ax.legend(bbox_to_anchor=(1550000, 130), bbox_transform=ax.transData, fontsize=label_fontsize)
# ax.legend(bbox_to_anchor=(1555000, 480), bbox_transform=ax.transData, fontsize=label_fontsize, ncol=2)
# ax.legend(bbox_to_anchor=(350000, 250), bbox_transform=ax.transData, fontsize=label_fontsize, ncol=2)
# ax.legend(loc='upper left', bbox_to_anchor=(300000, 400), bbox_transform=ax.transData, fontsize=label_fontsize-1, ncol=2, edgecolor='w')
ax.legend(loc=1, ncol=2)

# plt.subplots_adjust(top=0.97, right=0.98, left=0.1, bottom=0.28)
plt.tight_layout()



# plt.show()
plt.savefig("acc_compute_time.pdf", dpi=800)


