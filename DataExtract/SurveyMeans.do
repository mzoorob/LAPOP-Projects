use "C:\Users\zoorobmj\Desktop\grand_merge.dta
keep if year >= 2010
egen OK = anymatch(pais), values(10	15	41	13	8	9	3	2	4	1	11	40	14	16)
keep if OK

decode(pais), gen (Contry_String)
tostring(year), gen(year_string)
gen ctry_year = Contry_String + year_string

foreach var of varlist a4 	soct2 	idio2 	np1 	cp5 	cp6 	cp7 	cp8 	cp13 	cp20 	prot3 	jc15a 	vic1ext 	vic1hogar 	pole2n 	b2 	b3 	b4 	b6 	b10a 	b12 	b13 	b18 	b20 	b20a 	b21 	b21a 	b32 	b47a 	sd2new2 	sd3new2 	sd6new2 	ros4 	eff1 	eff2 	env1 	d5 	d6 	vb10 	dem2 	vb1 	clien1 	for1n 	np2 	sgl1 	vb2 	clien1na 	for7 	vb4new 	pol1 	vb101 	vb3n 	vb11_10 vb11_12 vb11_14 	vb20 	for4 	for5 	for6 	for6b 	for7b {
  lp_resc `var', gen(`var'_rescaled) min(0) max(100)
  gen `var'Weighted = `var'_rescaled * weight1500
  gen `var'Denom = .
  replace `var'Denom = weight1500 if !missing(`var')
}



gen byte touse=1
svymarkout touse
foreach var of varlist a4 	soct2 	idio2 	np1 	cp5 	cp6 	cp7 	cp8 	cp13 	cp20 	prot3 	jc15a 	vic1ext 	vic1hogar 	pole2n 	b2 	b3 	b4 	b6 	b10a 	b12 	b13 	b18 	b20 	b20a 	b21 	b21a 	b32 	b47a 	sd2new2 	sd3new2 	sd6new2 	ros4 	eff1 	eff2 	env1 	d5 	d6 	vb10 	dem2 	vb1 	clien1 	for1n 	np2 	sgl1 	vb2 	clien1na 	for7 	vb4new 	pol1 	vb101 	vb3n 	vb11_10 vb11_12 vb11_14 	vb20 	for4 	for5 	for6 	for6b 	for7b  {
  lp_resc `var', gen(`var'_resc) min(0) max(100)
 *sum for numerator
 egen  sum_`var'Weighted=total(`var'_resc*weight1500) if touse==1
 *sum for denominator
 egen `var'denom=total(weight1500) if !missing(`var') & touse==1
 *get the mean by dividing
 gen wt_mean_`var'=sum_`var'Weighted/`var'denom
 cap drop sum_`var'Weighted `var'denom
 *display the mean (wt_mean is a constant, so sum or tab will show it)
 tab wt_mean_`var'
 svy: mean `var'_resc
}
