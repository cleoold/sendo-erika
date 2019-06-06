from datetime import timedelta
from nonebot.default_config import *

## ::::::::::::::::..::::::::::::::::::::::::::::::::::::::::::::.............:::::::::::::::
## :::::::,,,,,::::::..:::,::::::::::::::::,,,:::::,,,,,,:,,:::..::::::::::::...:::::::::::,:
## ::,,,,,:::::::::::::..:::,:,:::::,,,:,::,,::,,,,::::::,::::.::::::::::::::::...:::::,,,,,:
## ::,,:::::::::::::,:::::::,::::::::::::::::::,,,,;;;,,,::::.::::,:::::::::,::::.:::::::::,:
## ::::,,,:::::,::::,,:::.::::::::::,,,:,::,,;i,::::,,::,;;:::::,::::::::::::::::::.:::::::,:
## :::::::::::::,,,:,;;ii;;,.::,::::,::,:;;::::::t,:,,,,:,:,;;,::::::::::::::::::::..::,,,:,:
## ::::::::::::,:,;:,:::,::::;:::::,,,;i,:::::::i:;,,,::,,,::,:;t::::::::::::::::::::.:::::,:
## :::::::,:,:,.;,::,:,::,,,::;:::,:ii;,:::,::,;:,:;,,,,::::::,,it;::::,::::::::::::::.:,::,:
## ::::::::,:,,i,:,,::,,,;,,,,:;,,,,:.:::::::,:;::,;i,,,,:::::;;;;,;,:,:::::::::::::::.::::,:
## :::::::,:,:;::,,:;iiii,,,,;;,i:.,;;,:::::,:;:::,,:;,,,:::::,:,,,:,;:,:::::::::::::::.:::,:
## ::::::::,:;,,:,;i;,::,,,,::,;t,,ii,:::::,,,;::,:,,:,,,:::::,:,,:,,,;:,:::::::::::,:::.::::
## :::::::::;,:,i,,,::,:,:,,;i;:.;i::::::,,,,i::,,,,,,,,,:::::::::,::,:,;::::::::::::,::.::::
## :::::::,;,:i;:,::,,,:,;iti,:.,,.:.:::;:,,;,,,,,,,,,,,,,:,:::::::,::,:,;:,:::::::::,::..:::
## ::::::::;:i,:,,,,::,;i;i:,i..:.:.:::;:,:,i:,,,,,,,,,,,,,,,,::,,:,:,:,:;,:,,,,:::::,:::.:::
## ::::::,,,i;:,,:,,:,ii,;:ii,,,:.:...;:,;,;;,:,,,,,,,,,;,,,,,,::;;,:,,,::;,::,,::::,::::.:::
## :::::,:;;,:,,,,,,;i;:;:t;,,;...:.:;:,;,;i,::,,,,,,,;,,;:,,,,,,,,i,::::,,;,,:,:::::::::.:::
## ::::,:,;,:,,,,,,,i,:;,j,.;,.....:.,:;;:i;,::,:,,,,,;,,;,,;,:,,:,:,;:,,::;,,:::::::::::.:::
## :::::;,,:,,:,::;i::;;i:::; .  .:.;,;,.,i;:::,:,,,,,,;,;;:i,,,;,,:,:i;,:,:;:,::::::::,::.::
## :,:,,,,::::,::,i:,;;t;:.;:....: ,:;,,:i;;::,:::,,,;,;;i,:t,,,;::,:,,t:::,;::,::::::::::.::
## :::,,,,:,::,,,t,,,it;,:;: :..: .;.;;.,t,,::,:::,,,i,i,i,,t,,,,::;,,,;,::,,,:,:::::::::::::
## ::,,::,::::::i,,,;i;;;,;.:. :..,:,,,.;i;::.,:::;,,j,t;i,,t;:,,,,,;:,;;::,,;:::::::::::.:::
## ::,:::,:::::,i:,,i;;,:i::,..:.,;.;::.ti;::.;::,,,;j,ti;,,j;,;,,,,i:,it,::,i,::::::::::.:::
## :;,,:,,,:,::i:,:;;,;,,,:;.:,.,;.i;; .ftt.:.;:,;:;t;t;tt,:j;,,,;,:;,i;i,:::i::,,,:,::::.:::
## :i::::,,:,,,;:,:t:;;:t:;,:,i,;i:tji.,ttt:..i:i,,ij:L,jj,,j;;,,i,,,;tji;::,t::,:,:::,::.:::
## ,,:::::,:,:;:,:;t,i,;j:;::;,i,,tijt,tijj:..i:i:it;ijtft,;i;;,,i,,,ittji::it::,::,tG;:.::::
## ;,,,:,::,,:;:,,t;;i:ij,;:;,,;i:jttj:titj:  i:,;ij:f;tfj,t,;i,;i:,:itttt;;ii:::;fDEL,:.::::
## ,::::::::::,:,:t,i;;jt;;,;i;ijifjtt,ttif,..t;,;f,tj:fft,j:;i,;i:,,ijttjiitt:;LGDELj:.:::::
## :,:::::::::,:,;i,i;iL;i,;;ttijjtttLLitif,..j;;t;ijtjtft:j:;i,,;:,,ifttjfiittDGDEGL;:.:::::
## :::::::::::,,:t,:titf;t,iitjfijf,ititG;f;.:j;titti,t;ti;i:;,,i,,,:tLttfLfiDEDEDLGt::::,,::
## ::::::::::::,:i:,t;tG,t;t;tLjt;f,ttt;Liji.:jifij;tttii.jj,i:,j,;,:tGjjjfGLEEEDLLL,::::,:::
## :,::::::::,:,:i:,tjtL;iii;Lftj;j:i,jif;fi.;titf,;ijit,j,f,t,;G:t;,tDjjjLEEDGGfjD;.,:::::::
## ::::::::::::,,i::tttL;;tiiGjiL:tjL:jit;Lt.iiGf,:jf;;;iL;f,t;iL:Lt,tEfjfLDGDGfjjj::::::::::
## :,,,::::,::::;,,:t;jfi;tijLLiLfWWWWLi,;fj:iiG;,tjititftiL;ttjj:fj,jKLjjLDGGjjfL:,:::::::::
## :,::::::,::,,i:,,f;jfi;ttGfLtDWEt#WWf:iii:ifL,,LjtijDLGGfitifjijt;jKDfjLEfLfffD,:,,:::::,:
## :,::::::,::,:;:,,f,fititLtjGfWK.GWW#Wi,:;tijtit,;;j;G;;tfLLLfiGftfjELffLEfDLGEL,,,:,::::,:
## :,::::::,::,:;::,j,j;tttG;fDLKf t,WWWt:.,itt;t:;,;,,j;ifjfjfL;LfiLEDEGfLDEKELGD,,:::::::,:
## :,:::::::::,,;::;j,j,jttf,DGGft..:KWW;.::.f,i,,:,;::tttfLtfiffLf;GKDfLGEEKGEEEt;:,,:::::,:
## :::::::::::::,::,i:i;fijL;EjL:i DKKKK::...i::;,,;jLGGGjiLL;LtfDjtEEfjffGKEffDDt,,:::::::,:
## :,:::::::::::,:,,;,,;itLGtDjL:, GGEDE.:....:.::GW######KLijtftLiLEGjfjfGWGffGDj,,:::::::,:
## :,::::::::::,,:,,,,;,:jDDtDLL:: fLEDL........::Dt,#######fLtiGjiEELjjfGEKGjfGDf,,:::::::,:
## :,,:,::::::::,,::,,:,,GDDjLLf,:.;LWDt.........:,,,##W####Wi;GiiGEELffGDEEDffLDf:,:::::::,:
## ,,,::::::::::,,,,,,:,;DDEDftj,,:,DfG:............::DWWW###DjtjiEKDLjGEKGEEGfLDL:,:::::::,:
## ;,:.:,::::::::,:::,,:fDDEEL;t,:,:jEG ............, fWWKW#W#t;fGDEDfGKEKLDEEfLDG,::::::::,:
## ,,,:.::::::::::,,,:,;LEDEDi;;;,::::............. jKKKKEK#K#fjtGDDDDEKGEDDLEDLDf,::::::::,:
## :;;,.:,:,:,::::::,,:jfDDEf:t,:::::...............jDWKDGKWE#GLG;DEEDKfEfGDGGEDDj,,:::,:::,:
## ,:,i,.:,:,:::::::,,;;,;;f,tjt::...... :.:....... ;DK#WEGLG;ttjfGGjELLDGfDDfLGji,:,::::::,:
## ,::,;:.,,:,::::::,,:,,,L,;jtj.........i,:.......::KfEDfK;,;tjfDfjGEjGGGfDDfffG;,,,::::::,:
## :,,:;,..;:,::::,:::,;,f;itt;L;........,,:.......:;EDfLGG;;tGjLffjKDjGjGLDDLjjjL:,,::::::,:
## ,;,,,;:.:,,,:,::,::,:j;itj;iff:......:........:::::jDEGi;,GLDGffDDjLLjfLDDGLGGft:,::::::,:
## .:i,;,,:.:;:,:::::,;;i:jtiittLi.:.............::::,;;;;;iLGLGjfLDLfL;tLLGLjtjGjj:,,:::::,:
## .:.i,,i,:.,:;,,::,;,,,ititif;ft;.....iE,:.......::,;;iitjfiGfffDGL;fiiLjtt;;ttLij;::::::,:
## ;,::.i,i,::,,,:,,,:;::titiL;,jjj;..:.:LfffD,...::::,,tf;ttLDffGLtGttGi;jfiiii;ttj;,i;,,:,:
## i;,::.ii,::.,,,,,:,:,:;tjLji;iGtt,:...jtjfL,....:::,jiififL,tGD;iLLijLi;ititt;,,itti,,,,,:
## :;;,:::tj,::.,i,:,,.,:ttjt;Gf;Lj,j...:;ttjj.....:::j,ij;jt,ifWDf,;KjijLi,;i;;tj;,::ijti;;,
## ,,;;,::.,;,..:t,,;:.:,ttittDG;jG;ti...:jjj:.....:;j:ttijt;;jK#GD;;;WEf,;jGLft;,j,;;;ittjti
## i,:;;,::......t:;;:.:it;iiDEDfifL;f;:........:::j;:f;jjt,;jK##EDE,,ttjGEEKWKf;,,,, :,i;:tt
## ..,;;t::.:.:..:t,;:.:t,;;iDEDGDGDEGDL:....::.:;i:ittfii;jL##W#EjEEDKGGDGDDDDEKE:,,jL;::,;,
## ::..:;;,:..:.:.t,i,:,j,;;fDEDGGGGGGGGL:.:....,jtLi.ji;ijfG###WEEtGKDEGGDDDDDEDEG.;,tffi,,;
## ;,::.:.:.:....:;i;,:,t;;tEDEDGDDGDDGGGG;;;tj;jfj;.it,tjjt####KEDKEEGLGLGGGGDGEEK;,;tfjGti,
## ,i;:::.........:ii;:;i;;tEDEDGDDGGGGGGKEEWt,:ti;.:t;jjttD####KEEKEGLLLLLLGGGGDEEi:;i,jjfji
## ;;i;:...........iit,,;,;LDGDDGDEGDGGGDWDDK,,ii;:.j,ftit;#WW#WKEKEGLLLLLLLGGGGDEKf,i,jt;LLj
## ...............::KL;:;,iDLGDDGDDDDGGGKEEDD.,fi,.,;fi;t;jW#W#KKKEGLLLLLLLLGGGGDEEfii:L;tfff
## ,,,,::.........::;GEt:iGDGDLDLEDEDGGEEDDK:itD,:.if;;i;fW####KWDLLLLLLLLLLLLGDDEELti,fLjffj
## ,;ii,:.........:::LEGtDGGGDGDGEEEDGGEDDDD,LjD.:;ji;;;tW###WWWDLLLLLLGGGLLLGGDEEEf:;,ff;fjj
## ;,,i;,.........:::LDLGfGGGGGDGEEEDGDDDDDLffGD,:jt;;;iG##WEKKGLLLLGDDDGGLLLGDEEEKt;:,fjjjLj
## ;,,,i,::........,ifELfjLGGLGEDKEDGGGGGGGLfLGG,:L,;;ifWWEDEEGLLLGDEDGLLLLLGDDEEEDii;,ffLfLt
## :,;,;,,::::..:..:fLDfLfLLGGGDDWDDLGGGLGGfjDGf;:i::,tLEDEEDfLLGEEEDGLLLLLGGDEEEEtL,i:fLGjfi
## ,,,;,;,,:::..:::,LLD:fL;GLLDDEEGLGGLLLLjfjDfG;,,.:ifEDDEGLGEEEEGLLLLLLLLGEEEEKGfji;:ffjLtj
## :::,,,;,,::::,::GDGKG:LiLDGGDKGLLLLLLffj.GELGji;:;:DDDDGGKKEDDLLLLLLLLLGDEEEEGEf,t:ifftjLE
## :,,:,;;;,,,,i.;GDL;GKfj;GLDDEELLLfLfLLti:DDfDti;,:iDDDDGWEEGLGLLLLLLLLGDEEEEDEDji;:ffLjjEE
## ::,,:,,iGiii,jDDDG;:GK:;fLGDEDLLEfLLfjf;fDfGGLtt:,LDEEDWEDGGLLLLLLLLLGDEEDEDDEDtt,iLftfLDE
## :::,::;fDjiiEEDDELLj:LD,LfLLELLfGEfftif:GE,GGfjij;GDDEWWGGGLLLLLLLLLGEEEDEDGKEGi;;fLf;LLDE
## :::::,:EE;tWWWKEGGGfi:Df,LLLGGfffLDfij,tDf:GDjtj,G;fEEWEGGGLLLLLLLLGEEEDDELEEKLt,jGLf,GjED
## :::::,i#WWW#WWDGGG;jLL;iG:ffGLDGLLLLLG.GL,jGG;jiGKGj;EKDGGLLLLLLLLGEEGGEDtEKEWL;tDELL,LGLE
## ::::,:LW#W#WKDDGG;tGf,Gf,L;LLLGDGGGGGG,Gi,LGG;j;EDLDiGDGGLLLLLLLLDEDGGDDEGEEEWL;fDKDf;jDLG
## ::::,,LWW##EEEDDijGj;LGfG;j;fLLGDDGDGLGG:;GGGii;DLLLGjEGGLLLLLLLDEDGGDDEGKEEKKLiGEEKf;ijDG
## :::::,.GWWEEDEDtfGj;LLfGLGitLLLLGDDDtLDj:tLGGL;tGLLGEjDGLLLLLLGDEGGGDDEEjEEEKEGtDKEEfi,tiG
## ::::.::DKEEEELiGEtfGGLLLLLLf;LLLGLEE:GL,.;LDDL,GLLLDEfGLLLLLLLEDLGGDEEEEtEEEEEDfEEDGEt,it;
## ::::::,GEEEDtfDEjLDDGGGGLLLLjtLLLGDEtLG:,.fGLifLLGEEDLGGLLfLGELLGGDDEEEEtEEEEEELEDDDEG;,it
## :::::,,,;GtGEDjfEEEDDGGGLLLLfLLLLLGLDG:.:.tLfGGGGGGGGGGLLGDDGLGLGDEEEEEEfKEKKEEfEEEDGGD;i,
## :,,:,:;::iGELtGEEEEEEDGGLLGLLLLGGGLGLG:,..ttjDDDDGEGGGGGDEDLLLGGDDEEEEKEGKKKEEEfEEDGGLGL;;
## :::::::,,,itfDEEEEEEEDDGGGLLLLLLGGLLGLDi,:tjGDDDDEDGGDEEDLLLGLGGDEEEEEKKEKKEEEEDGDGGGGGDj;
## :::::,:,;,,tEDEEEEEEEEDDGGLLLLLLGGLLLGLL:,jGEEEEEEGEKEEDLLLLGGDDEEEEEEWWWEEEEDEDGGGGGGGGE,
## :::::::::,;;EDDEEEEEEEEDDGGLLLLLGGGLLLGGL;GDKKKKKDKEEEGfLLGLGGDEEEEEEKWWEGKEEDGGGGGGGGDGGi
## ::::::::,:,DDEKEEEEEEEEEEDGGGLLLGDDGLLLGGKDEWKWEKEKDLLLLLLLGGDEEEEEKWKKKEKDEDGGGGGDDDDGLLf
## :::::::::,:EEEEEEEEEEEEEEDDGGLLLGDDGLLLLLDEEEKKWKEDLLLLLLLLGDEEEEEEWKKKKEKEDGGGGGDDDDGLGDt
## ::::::::,:fGEEKEEEEEEEEEEEEDGGLLGDDDGLLLGGEEEDEGGGLLLLLLGGGGDEEEEEKKEEEKKEEGGGGGDDEDGGGEEt
## :::::::::,DEEDDEEDEEEEEEEEEEDGLLLGEDDLLLLGEEDKDKEEEEDDDGGLGDEEEEEKWEEEEKKEEGGGDEEEDGDDEEEL
## ::,::,:::jDDEDEDDDDEEEEEEEEEDGGLLGEEDGLLLLDEEEDKKGGEEEEEEGGDEEEEKWEEEKKKKEDGDEEDGGDEEKEGDG
## :::::::::DDDGEGGDGGDEEEEEEEEDDGLLLDEDGLLLLGDEDDDKEKLLGDDEGGDEEEEKKEEEKKKKEDEEEDDDEEEEGLLGD

SUPERUSERS = { }
COMMAND_START = {''}
NICKNAME = {'千堂', '千堂 瑛理華', '千堂瑛理華', '千堂瑛理华',
            '千堂 瑛理华', '千堂瑛里华', '千堂 瑛里华', '瑛里华', '瑛理华', 'erika'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=2)

HOST = '172.17.0.1'
PORT = 8080

# PLUGIN-SPECIFIC SETTINGS

AMAP_WEATHER_API_KEY = ''

OPENWEATHERMAP_API_KEY = ''

GLOT_RUN_TOKEN = ''

