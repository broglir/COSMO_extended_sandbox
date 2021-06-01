import xarray as xr
import glob
import subprocess

laf_path = glob.glob('./output/ifs2lm/laf209?1101*.nc')[0]
laf = xr.open_dataset(laf_path, decode_cf=False)
replace = xr.open_dataset(
'/project/pr94/lhentge/results_pp_testatlantic/results_ppcc_atl_EXPL/int2lm_out/W_SO_spinup_NOV_selbox_corr2.nc',
decode_cf=False)

laf['W_SO'].values = replace['W_SO'].values

try:
	laf['rotated_pole'] = laf['rotated_pole'].squeeze()
except:
	pass

#laf.close()
laf.to_netcdf(f'{laf_path}_new')

subprocess.run(f'mv {laf_path} {laf_path}_old', shell=True)
subprocess.run(f'mv {laf_path}_new {laf_path}', shell=True)

print(f'saved {laf_path}')
