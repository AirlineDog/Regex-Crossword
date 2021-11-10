# Regex-Crossword
**A python script able to find the solution of a regex crosword.**

All you need is to convert your Regex Crossword into a csv and a txt file as in the following example.<br>

![Regex-Cross](https://user-images.githubusercontent.com/72792044/141176419-b1b645dc-d280-4dad-bdf5-569d123550f6.png)

- [laughs.txt](https://github.com/AirlineDog/Regex-Crossword/blob/main/laughs.txt)

Every line will contain a regex pattern 

```
L(OL)+
H(EH)+
MWA(HA)+
(AH)+A+
(HO)+
ROT?FL
HE(HE)+
HA+
K(EK)*E
TE(HE+)+
LO+L
(JA)+
(HAR+)+
LAW*L
HAHA*
LULZ
```
- [laughs.csv](https://github.com/AirlineDog/Regex-Crossword/blob/main/laughs.csv)

Every line will contain the word number, a sting of dots and letters to represent the known and unknown characters, pairs of numbers where the first is a word number that intercepts and the second one is the index of the intersection
```
0,......,15,0
2,....,1,0,5,1
4,........,9,2,13,0,15,3
6,.......,5,3,7,2,9,4,11,0
8,....,1,3
10,.....,11,2,13,4
12,...,1,5,3,0
14,..........,3,2
1,......,2,0,8,1,12,1
3,...,12,2,14,1
5,....,2,3,6,0
7,LULZ,6,2
9,.....,4,0,6,4
11,....,6,6,10,1
13,........,4,4,10,3
15,.....,0,4,4,6
```
Running the script you must include these files as arguments:
```
py .\re_crossword.py .\hex.csv .\hex.txt
```
The script will print the solution in this form:

```
0   HAHA*   HAHAAA
1   HE(HE)+   HEHEHE
2   (HO)+   HOHO
3   HA+   HAA
4   TE(HE+)+   TEHEHEHE
5   LO+L   LOOL
6   L(OL)+   LOLOLOL
7   LULZ   LULZ
8   K(EK)*E   KEKE
9   ROT?FL   ROTFL
10   MWA(HA)+   MWAHA
11   LAW*L   LAWL
12   H(EH)+   HEH
13   (HAR+)+   HARRHARR
14   (JA)+   JAJAJAJAJA
15   (AH)+A+   AHAHA
```
