@echo off
:A
copy *.css zzcomp.css
cd..
copy idealist\zzcomp.css themes\idealist.css
copy idealist\zzcomp.css snippets\idealist.css

pause 
cd idealist
goto A