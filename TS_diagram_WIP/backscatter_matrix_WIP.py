import numpy as np


def compute_backscatter_mat(df_backscatter,time,depth,len_sampling):
	# Init. Sv_matrix
	u_time_Sv = np.unique(time)
	u_depth_Sv = np.unique(depth)
	Sv_mat = np.zeros((len(u_time_Sv), len(u_depth_Sv)))
	for h in range(len(Sv_ancho_mission)):
		t = np.where(u_time_Sv == Sv_ancho_mission['Time'][h])[0][0]
		d = np.where(u_depth_Sv == Sv_ancho_mission['Depth_start'][h])[0][0]
		Sv_mat[t, d] = Sv_ancho_mission['Sv'][h]
	Sv_mat[Sv_mat != 0] = 10 ** (Sv_mat[Sv_mat != 0] / 10)  # Convert to linear
	tq, dq = np.meshgrid(time, -depth)  # Negative depth to make it consistent with the original code
	Sv_matQ = scipy.interpolate.interp2d(u_depth_Sv, u_time_Sv, Sv_mat.T)(dq, tq)
	#  %%%%%%%%%% INTERP 2 %%%%%%%%%%  and  Sv_matQ=interp2(u_depth_Sv,u_time_Sv, Sv_mat, -dq,tq)';
	Sv_matQ[Sv_matQ != 0] = 10 * np.log10(Sv_matQ[Sv_matQ != 0])  # Convert back to log
	Sv_matQ[Sv_matQ == 0] = np.nan  # 0s to nan
	# if 'i1' in locals() and 'i2' in locals():  # If filtering date # if exist("i1","var") && exist("i2","var")
	#     Sv_matQ = Sv_matQ[i1:i2, :]
	#     Sv_matQ = Sv_matQ.flatten()
	# else:  # If not filtering date # else
	#     Sv_matQ = Sv_matQ.flatten()
	# Flatten the matrix
	Sv_matQ = Sv_matQ.flatten()


compute_backscatter_matrix()