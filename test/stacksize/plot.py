
import os, sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.colors import hsv_to_rgb



label_fontsize = 12


fig, axes = plt.subplots(1, 1, figsize=(4, 3))

ax = axes

ds_list = range(0, 4)
stacksize_uvm = [14840, 14840, 14912, 14912] # median
stacksize_uvm = []
stacksize_uvm_err_set = [(14808, 15107), (14844, 15059), (14844, 14954), (14844, 14954)]
for a in stacksize_uvm_err_set:
	stacksize_uvm.append((a[0]+a[1])/2)
stacksize_uvm_err = []
for a in zip(stacksize_uvm, stacksize_uvm_err_set):
	mean = a[0]
	b0 = a[1][0]
	b1 = a[1][1]
	stacksize_uvm_err.append(max(mean-b0, b1-mean))

stacksize_ach = [15680, 15696, 15696, 15696] # median
stacksize_ach = []
stacksize_ach_err_set = [(15608, 15705), (15583, 15716), (15624, 15721), (15624, 15721)]
for a in stacksize_ach_err_set:
	stacksize_ach.append((a[0]+a[1])/2)
stacksize_ach_err = []
for a in zip(stacksize_ach, stacksize_ach_err_set):
	mean = a[0]
	b0 = a[1][0]
	b1 = a[1][1]
	stacksize_ach_err.append(max(mean-b0, b1-mean))





ind = np.arange(len(ds_list))
width = 0.2


print stacksize_ach[3]-stacksize_uvm[3], "B"
print "%.2f%%" % (100.0*(stacksize_ach[3]-stacksize_uvm[3])/stacksize_uvm[3])


# line = ax.plot(ds_list, stacksize_uvm, "--x", label="UVM", color="#1f77b4")
rects1 = ax.bar(ind - width/2, stacksize_uvm, width, yerr=stacksize_uvm_err, edgecolor='k', color="lightgray", label='UVM')

# line = ax.plot(ds_list, stacksize_ach, "--^", label="pointerchain", color="#ff7f0c")
rects1 = ax.bar(ind + width/2, stacksize_ach, width, yerr=stacksize_ach_err, edgecolor='k', color="gray", label='pointerchain')



# line = ax.plot(ds_list, cuda_gflops['advVel'], "--v", label="CUDA-AdvanceVelocity", color='#2ca02c')
# print line[0].get_color()

# ax.plot(ds_list, acc_gflops['force'], "-x", label="ACC-ComputeForce")
# ax.plot(ds_list, acc_gflops['advPos'], "-^", label="ACC-AdvancePosition")
# ax.plot(ds_list, acc_gflops['advVel'], "-v", label="ACC-AdvanceVelocity")

# ax.set_yscale('log')

ax.set_xlabel('Level', fontsize=label_fontsize)
ax.set_ylabel('Stack size (Bytes)', fontsize=label_fontsize)

for tick in ax.yaxis.get_major_ticks():
	tick.label.set_fontsize(label_fontsize-2)



ax.set_xticks(ds_list)
ds_list_title = [format(_ss, ',') for _ss in ds_list]
ax.set_xticklabels(ds_list_title, fontsize=label_fontsize-2)

ax.set_yticks(range(0, 20001, 5000))
number_comma = [format(_ss, ',') for _ss in range(0, 20001, 5000)]
ax.set_yticklabels(number_comma, fontsize=label_fontsize-2)

# ax.legend(bbox_to_anchor=(1550000, 130), bbox_transform=ax.transData, fontsize=label_fontsize)
# ax.legend(bbox_to_anchor=(1555000, 480), bbox_transform=ax.transData, fontsize=label_fontsize, ncol=2)
# ax.legend(bbox_to_anchor=(350000, 250), bbox_transform=ax.transData, fontsize=label_fontsize, ncol=2)
# ax.legend(loc='upper left', bbox_to_anchor=(300000, 400), bbox_transform=ax.transData, fontsize=label_fontsize-1, ncol=2, edgecolor='w')
ax.legend(loc=1, ncol=2)

# plt.subplots_adjust(top=0.97, right=0.98, left=0.1, bottom=0.28)
plt.tight_layout()



# plt.show()
plt.savefig("stacksize.pdf", dpi=800)


