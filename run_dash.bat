@echo off
echo Now downloading PDFs from https://grad.uw.edu/about-the-graduate-school/statistics-and-reports/admissions-statistics/
python Download_PDFs.py $1
echo Finished downloading PDFs. 
echo Now scraping statistics...
python Admission_Stats.py $1
echo Finished with statistics.
echo Implementing Dashboard elements....
python dashboard.py $1
echo Exit when ready