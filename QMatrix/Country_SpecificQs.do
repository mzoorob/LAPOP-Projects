** this program reads in the grand merge file and prints each country specific question code to the console
** read the grand_merge file
use "C:\Users\zoorobmj\Desktop\grand_merge.dta"

* this loop will get every country specific question
** to instead find any particular country, delete outer loop and replace pais with number equal to pais of interest (line 13)
*** plausibly one could toggle with r(c) == [num] if you wanted to, say, find questions asked in <5 countries, etc
foreach i of num 1/17 21/29 40 41 { 
	foreach var of varlist q1-q11nr {
		capture quietly tab `var' pais
		* I know it's country specific if r(c) == 1
		if r(c) == 1 {
		quietly sum `var' if pais == `i'
		* if it's ctry specific AND has results for Nicaragua, it is a Nicaragua-only question
			if r(N) > 0 {
				display "`var'"
				}
		}
	}
}
