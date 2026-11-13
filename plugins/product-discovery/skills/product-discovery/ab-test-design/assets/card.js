'use strict';
const I18N = {
  "en": {
    "workspace": "Experiment card",
    "print": "Print / PDF",
    "savedPlan": "A/B test plan",
    "demo": "EXAMPLE · All numbers are illustrative. This card does not describe a completed experiment.",
    "hypothesis": "What we are testing",
    "control": "Current experience",
    "treatment": "Proposed change",
    "population": "Who takes part",
    "weekly": "Unique people / week",
    "allocation": "Random A / B assignment",
    "primary": "How we measure success",
    "baseline": "Baseline",
    "target": "Detection target",
    "recruitment": "Recruitment",
    "readout": "When we can read the result",
    "guardrails": "What else we watch",
    "safetyNote": "No significant drop means no deterioration was detected. A small drop can go unnoticed.",
    "recommendation": "Is this test worth running?",
    "decisionRule": "What happens after the test?",
    "before": "Before launch",
    "calculator": "Do we have enough people?",
    "scenarioNote": "Change the numbers to explore sample size and duration. The saved plan stays unchanged.",
    "unsupported": "This design requires a different calculation. The independent-proportions calculator is disabled.",
    "effectUnit": "Effect unit",
    "relative": "% relative",
    "points": "percentage points",
    "scenarioTarget": "Scenario: baseline → target",
    "power": "Chance of detecting the assumed change",
    "powerExplain": "Chance of detecting the assumed improvement if it is real. We aim for at least 80%.",
    "available": "Available / variant",
    "needed": "Required / variant",
    "neededDays": "Required recruitment",
    "scenarioReadout": "Full scenario readout",
    "mde": "Minimum detectable change at this traffic and duration",
    "reset": "Reset to plan",
    "export": "Save scenario",
    "defaults": "Two proportions · A/B 50/50 · two-sided test · α = 0.05 · target power 80% · normal approximation.",
    "after": "After collecting data",
    "results": "Results after data collection",
    "observedNote": "Enter actual counts after the test ends. Every participant needs their full outcome window.",
    "observedCounts": "Assignments and outcomes",
    "variant": "Variant",
    "assigned": "Assigned people",
    "successes": "Metric events",
    "complete": "The test and every participant's outcome window are complete.",
    "quality": "A/B assignment and data collection have been checked.",
    "footer": "A plan, not a result. Always evaluate guardrails alongside the primary metric.",
    "method": "Method and sources",
    "methodText": "Power: pooled null variance and unpooled alternative variance. Results: two-sided two-proportion z-test and approximate 95% Wald interval for the difference. Assignment check: chi-square with diagnostic threshold 0.001. Requires independent observations; does not cover continuous metrics, clusters or repeated peeking.",
    "draft": "Needs refinement",
    "revise": "Revise the plan",
    "ready": "Worth running",
    "noGuardrail": "Guardrail definitions are missing.",
    "days": "days",
    "users": "people",
    "effectLabel": "Change to detect",
    "durationLabel": "Recruitment days",
    "empty": "Enter the missing numbers to assess feasibility. No assumptions are filled in for you.",
    "badTarget": "The target must be strictly between 0% and 100%. Change the effect magnitude or unit.",
    "sparsePlan": "Too few expected events for a reliable normal approximation. A rare-event assessment is needed.",
    "adequate": "These numbers should provide enough people to detect the assumed change.",
    "underpowered": "This scenario is underpowered. Recruit for longer or consider a change that could credibly produce a larger effect. If neither makes sense, skip this A/B test.",
    "deadline": "Full readout falls after the decision deadline.",
    "longer": "At the assumed effect, full readout needs approximately",
    "unreachable": "Even an extreme change cannot reach 80% power with this sample.",
    "sizingNote": "Recruit for at least 14 days, then in full weeks. Add the last participants' outcome windows. Check holidays and promotions before starting.",
    "emptyResults": "Waiting for actual data. Planned sample sizes and forecasts are not experiment results.",
    "invalidCounts": "Enter non-negative integer event counts no greater than assignments. Each variant needs at least one person.",
    "sparseResults": "Too few events or non-events in at least one variant. The approximate z-test is unreliable; use another method.",
    "srm": "Assignment differs from 50/50 (SRM p < 0.001). Pause interpretation and investigate.",
    "provisional": "Calculation preview. Final interpretation requires the planned horizon, mature outcomes and verified data. Do not stop at the first significant reading.",
    "significant": "The difference between A and B is statistically significant. Check the business target and the other important metrics before deciding.",
    "notSignificant": "These data do not resolve whether the variants differ.",
    "notEnoughActual": "Fewer people were recruited than the saved plan requires. Check the agreed stopping rule before interpreting.",
    "absolute": "Difference B − A",
    "ci": "95% interval for difference",
    "pvalue": "p-value (two-sided)",
    "rates": "A / B rates",
    "scenarioExport": "Scenario for discussion; plan text needs review.",
    "durationRule": "Recruit for at least 14 days, then in full weeks: 21, 28, 35 days, etc.",
    "noRun": "Do not run now",
    "scenarioReady": "Enough traffic"
  },
  "pl": {
    "workspace": "Karta eksperymentu",
    "print": "Drukuj / PDF",
    "savedPlan": "Plan testu A/B",
    "demo": "PRZYKŁAD · Wszystkie liczby są ilustracyjne. Ta karta nie opisuje przeprowadzonego testu.",
    "hypothesis": "Co sprawdzamy",
    "control": "Wersja obecna",
    "treatment": "Proponowana zmiana",
    "population": "Kto bierze udział",
    "weekly": "Unikalne osoby / tydzień",
    "allocation": "Losowy przydział A / B",
    "primary": "Po czym poznamy sukces",
    "baseline": "Wartość bazowa",
    "target": "Cel do wykrycia",
    "recruitment": "Zbieranie próby",
    "readout": "Kiedy poznamy wynik",
    "guardrails": "Na co jeszcze patrzymy",
    "safetyNote": "Brak istotnego spadku oznacza, że nie wykryliśmy pogorszenia. Mały spadek może pozostać niezauważony.",
    "recommendation": "Czy warto zrobić ten test?",
    "decisionRule": "Co zrobimy po teście?",
    "before": "Przed uruchomieniem",
    "calculator": "Czy wystarczy nam osób?",
    "scenarioNote": "Zmień liczby i sprawdź, jak wpływają na potrzebną próbę i czas. Zapisany plan pozostaje bez zmian.",
    "unsupported": "Ten projekt wymaga innej metody obliczeń. Kalkulator dwóch niezależnych odsetków jest wyłączony.",
    "effectUnit": "Jednostka zmiany",
    "relative": "% względnie",
    "points": "punkty procentowe",
    "scenarioTarget": "Scenariusz: wartość bazowa → cel",
    "power": "Szansa wykrycia założonej zmiany",
    "powerExplain": "Szansa wykrycia założonej poprawy, jeśli rzeczywiście wystąpi. Celujemy w co najmniej 80%.",
    "available": "Dostępne / wariant",
    "needed": "Potrzebne / wariant",
    "neededDays": "Potrzebne zbieranie próby",
    "scenarioReadout": "Pełny odczyt scenariusza",
    "mde": "Najmniejsza wykrywalna zmiana przy tym ruchu i czasie",
    "reset": "Wróć do planu",
    "export": "Zapisz scenariusz",
    "defaults": "Dwa odsetki · A/B 50/50 · test dwustronny · α = 0,05 · moc docelowa 80% · przybliżenie normalne.",
    "after": "Po zebraniu danych",
    "results": "Wynik po zebraniu danych",
    "observedNote": "Wpisz rzeczywiste liczby po zakończeniu testu. Każda osoba musi mieć pełny czas na wykonanie mierzonej czynności.",
    "observedCounts": "Liczebności i konwersje",
    "variant": "Wariant",
    "assigned": "Przypisane osoby",
    "successes": "Zdarzenie metryki",
    "complete": "Test i czas na zebranie wyników wszystkich osób już się zakończyły.",
    "quality": "Sprawdzono, że przydział A/B i zbieranie danych działają poprawnie.",
    "footer": "Plan, nie wynik. Zmiana metryki głównej zawsze wymaga oceny zabezpieczeń.",
    "method": "Metoda i źródła",
    "methodText": "Moc: wariancja łączona pod hipotezą zerową, osobne wariancje pod alternatywą. Wynik: dwustronny test z dla dwóch odsetków i przybliżony 95% przedział Walda dla różnicy. Kontrola przydziału: chi-kwadrat, próg diagnostyczny 0,001. Metoda wymaga niezależnych obserwacji; nie obejmuje metryk ciągłych, klastrów ani korekty za wielokrotne podglądanie.",
    "draft": "Do dopracowania",
    "revise": "Zmień plan",
    "ready": "Test ma sens",
    "noGuardrail": "Brakuje definicji zabezpieczeń.",
    "days": "dni",
    "users": "osób",
    "effectLabel": "Zmiana do wykrycia",
    "durationLabel": "Dni zbierania próby",
    "empty": "Uzupełnij brakujące liczby, aby sprawdzić wykonalność. Nie przyjmujemy ich za Ciebie.",
    "badTarget": "Cel musi mieścić się między 0% a 100%. Zmień wielkość efektu lub jego jednostkę.",
    "sparsePlan": "Za mało oczekiwanych zdarzeń do wiarygodnego przybliżenia normalnego. Potrzebna ocena rzadkich zdarzeń.",
    "adequate": "Przy tych liczbach powinno wystarczyć osób, żeby wykryć zakładaną zmianę.",
    "underpowered": "Ten scenariusz ma za małą moc. Wydłuż zbieranie próby lub rozważ zmianę, która wiarygodnie może dać większy efekt. Jeśli to nie ma sensu, zrezygnuj z tego A/B.",
    "deadline": "Pełny odczyt wypada po zadanym terminie decyzji.",
    "longer": "Przy założonym efekcie pełny odczyt wymaga około",
    "unreachable": "Nawet skrajna zmiana nie osiągnie mocy 80% przy tej próbie.",
    "sizingNote": "Zbieramy dane przez minimum 14 dni, potem pełnymi tygodniami. Na końcu czekamy na rejestrację i aktywację ostatnich osób. Przed startem sprawdź święta i promocje.",
    "emptyResults": "Czeka na rzeczywiste dane. Planowana próba i prognozy nie są wynikami testu.",
    "invalidCounts": "Podaj całkowite, nieujemne liczby zdarzeń nie większe od liczby przypisanych osób. Każdy wariant musi mieć co najmniej jedną osobę.",
    "sparseResults": "Za mało zdarzeń lub ich braków w co najmniej jednym wariancie. Przybliżony test z jest niewiarygodny; potrzebna inna metoda.",
    "srm": "Przydział odbiega od 50/50 (SRM p < 0,001). Wstrzymaj interpretację i sprawdź przyczynę.",
    "provisional": "Podgląd obliczeń. Interpretacja końcowa czeka na ustalony horyzont, dojrzałe wyniki i kontrolę danych. Nie kończ testu po pierwszym istotnym odczycie.",
    "significant": "Różnica między A i B jest istotna statystycznie. Przed decyzją sprawdź, czy osiągamy cel i czy inne ważne wyniki się nie pogorszyły.",
    "notSignificant": "Wynik nie rozstrzyga, czy warianty się różnią.",
    "notEnoughActual": "Zebrano mniej osób niż wymaga zapisany plan. Przed interpretacją sprawdź zgodność z ustaloną regułą zakończenia.",
    "absolute": "Różnica B − A",
    "ci": "95% przedział różnicy",
    "pvalue": "p-value (dwustronne)",
    "rates": "Wartości A / B",
    "scenarioExport": "Scenariusz do omówienia; tekst planu wymaga przeglądu.",
    "durationRule": "Zbieraj próbę przez co najmniej 14 dni, potem pełnymi tygodniami: 21, 28, 35 dni itd.",
    "noRun": "Nie uruchamiaj teraz",
    "scenarioReady": "Ruch wystarcza"
  }
};
const data=JSON.parse(document.getElementById('card-data').textContent);
const t=I18N[data.language], locale=data.language;
const $=id=>document.getElementById(id), set=(id,value)=>{$(id).textContent=value;};
const num=(x,d=0)=>Number.isFinite(x)?x.toLocaleString(locale,{maximumFractionDigits:d}):'…';
const pct=x=>Number.isFinite(x)?`${num(x*100,3)}%`:'…';
const days=x=>Number.isFinite(x)?`${num(x)} ${t.days}`:'…';
const pp=x=>`${num(x*100,3)} pp`;
const pformat=p=>p<0.0001?'< 0.0001':num(p,4);
document.querySelectorAll('[data-i18n]').forEach(el=>{el.textContent=t[el.dataset.i18n];});
document.title=`A/B · ${data.title}`;
['title','hypothesis','control','treatment','population','metric','metric_definition','baseline_source','recommendation','decision_rule'].forEach(k=>set(k,data[k]));
$('demo').hidden=!data.illustrative;
const saved=data.calculator_supported?ABStats.plan(data):{error:'unsupported'};
const blocked=[...data.blockers];
if(!data.guardrails.length) blocked.push(t.noGuardrail);
data.guardrails.forEach(g=>{
 const item=document.createElement('article');item.className='guardrail';
 for(const [tag,key,cls] of [['h3','name',''],['p','definition',''],['p','limit','limit']]){
  const el=document.createElement(tag);el.textContent=g[key];el.className=cls;item.append(el);
 } $('guardrails').append(item);
});
blocked.forEach(text=>{const li=document.createElement('li');li.textContent=text;$('blockers').append(li);});
$('blockers').hidden=!blocked.length;
set('saved-traffic',data.weekly_users===null?'…':`${num(data.weekly_users)} ${t.users}`);
set('saved-baseline',pct(data.baseline));set('saved-target',pct(saved.target));
set('saved-effect',data.effect===null?'…':`${data.direction==='down'?'−':'+'}${num(data.effect,3)} ${data.effect_type==='pp'?'pp':t.relative}`);
set('saved-duration',days(data.recruitment_days));
set('saved-readout',days([data.recruitment_days,data.primary_window_days,data.guardrail_window_days].every(Number.isFinite)?data.recruitment_days+Math.max(data.primary_window_days,data.guardrail_window_days):null));
const afterDeadline=r=>data.max_readout_days!==null&&Number.isFinite(r.readout)&&r.readout>data.max_readout_days;
const numericalPass=r=>!r.error&&!r.sparse&&r.power>=0.8&&!afterDeadline(r);
const ready=numericalPass(saved)&&!blocked.length&&!data.illustrative;
const beyondUsefulTime=r=>!r.error&&!r.sparse&&data.max_readout_days!==null&&(r.required_readout>data.max_readout_days||afterDeadline(r));
function badge(id,label,tone){set(id,label);$(id).className=`badge ${tone}`;}
const savedTone=ready?'good':beyondUsefulTime(saved)?'danger':'caution';
badge('status',ready?t.ready:savedTone==='danger'?t.noRun:saved.error||blocked.length?t.draft:t.revise,savedTone);
$('status').closest('.decision').dataset.tone=savedTone;
$('effect-type').setAttribute('aria-label',t.effectUnit);
$('effect-type').options[0].title=t.relative;$('effect-type').options[1].title=t.points;
const specs=[
 {key:'baseline',label:t.baseline,min:0.0001,max:99.9999,step:0.1,unit:'%',scale:100},
 {key:'weekly_users',label:t.weekly,min:1,max:1000000,step:1,unit:'',log:true},
 {key:'effect',label:t.effectLabel,min:0.001,max:100,step:0.1,unit:'',scale:1},
 {key:'recruitment_days',label:t.durationLabel,min:14,max:364,step:7,unit:t.days,scale:1}
];
const scenario={...data};
specs.forEach(s=>{
 const wrapper=document.createElement('div');wrapper.className='control';
 const head=document.createElement('div');head.className='control-head';
 const label=document.createElement('label');label.htmlFor=`value-${s.key}`;label.textContent=s.label;
 const holder=document.createElement('div');holder.className='input-unit';
 const input=document.createElement('input');input.type='number';input.id=label.htmlFor;input.min=s.min;input.step=s.key==='recruitment_days'?'7':'any';input.max=s.key==='baseline'?99.9999:1e9;
 const unit=document.createElement('span');unit.textContent=s.unit;holder.append(input);
 if(s.key==='effect')holder.append($('effect-type'));else if(s.unit)holder.append(unit);
 head.append(label,holder);
 const range=document.createElement('input');range.type='range';range.id=`range-${s.key}`;range.setAttribute('aria-label',s.label);range.min=s.log?0:(s.key==='baseline'||s.key==='effect'?0.1:s.min);range.max=s.log?6:s.max;range.step=s.log?0.01:s.step;
 wrapper.append(head,range);$('controls').append(wrapper);
 s.input=input;s.range=range;
 input.addEventListener('input',()=>{
  const v=input.value===''?null:input.valueAsNumber;
  scenario[s.key]=v===null?null:v/(s.scale||1);
  syncRange(s,v);calculate();
 });
 range.addEventListener('input',()=>{
  const v=s.log?Math.round(10**range.valueAsNumber):range.valueAsNumber;
  input.value=Number(v.toPrecision(10));scenario[s.key]=v/(s.scale||1);calculate();
 });
});
function syncRange(s,v){
 if(v===null||!Number.isFinite(v))return;
 const rv=s.log?Math.log10(Math.max(1,v)):v;
 s.range.max=Math.max(s.log?6:s.max,rv);s.range.value=rv;
}
function reset(){
 Object.assign(scenario,data);
 specs.forEach(s=>{const v=data[s.key]===null?null:data[s.key]*(s.scale||1);s.input.value=v===null?'':Number(v.toPrecision(10));syncRange(s,v);});
 $('effect-type').value=data.effect_type;calculate();
}
function calculate(){
 const r=data.calculator_supported?ABStats.plan(scenario):{error:'unsupported'};
 ['power','available','needed','needed-days','scenario-readout','mde','scenario-target'].forEach(id=>set(id,'…'));
 $('power-fill').style.width='0%';$('calc-verdict').className='verdict';set('sizing-note','');
 badge('scenario-status',t.draft,'caution');
 if(r.error){set('scenario-verdict',r.error==='target'?t.badTarget:r.error==='unsupported'?t.unsupported:r.error==='duration'?t.durationRule:t.empty);return;}
 set('scenario-target',`${pct(scenario.baseline)} → ${pct(r.target)}`);
 set('power',r.power===null?'…':pct(r.power));$('power-fill').style.width=`${(r.power||0)*100}%`;
 set('available',num(r.n));set('needed',num(r.need));set('needed-days',days(r.days));set('scenario-readout',days(r.readout));
 set('mde',r.mde===null?t.unreachable:`${pp(r.mde)} · ${num(r.mde/scenario.baseline*100,3)} ${t.relative}`);
 let verdict=r.sparse?t.sparsePlan:r.power>=0.8?t.adequate:t.underpowered;
 if(r.power<0.8&&r.required_readout!==null)verdict+=` ${t.longer} ${days(r.required_readout)}.`;
 if(afterDeadline(r)||(r.power<0.8&&data.max_readout_days!==null&&r.required_readout>data.max_readout_days))verdict+=` ${t.deadline}`;
 const tone=numericalPass(r)?'good':beyondUsefulTime(r)?'danger':'caution';
 set('scenario-verdict',verdict);$('calc-verdict').className=`verdict ${tone}`;
 badge('scenario-status',tone==='good'?t.scenarioReady:tone==='danger'?t.noRun:t.revise,tone);
 set('sizing-note',t.sizingNote);
}
$('effect-type').addEventListener('change',()=>{scenario.effect_type=$('effect-type').value;calculate();});
$('reset').addEventListener('click',reset);$('print').addEventListener('click',()=>window.print());
$('export').addEventListener('click',()=>{
 const out={...scenario,blockers:[...data.blockers,t.scenarioExport]};
 const url=URL.createObjectURL(new Blob([JSON.stringify(out,null,2)],{type:'application/json'}));
 const a=document.createElement('a');a.href=url;a.download='ab-scenario.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
function resultMessage(message,cls=''){const p=document.createElement('p');p.className=`verdict ${cls}`;p.textContent=message;$('result-output').append(p);}
function results(){
 $('result-output').replaceChildren();
 if(!data.calculator_supported){resultMessage(t.unsupported);return;}
 const fields=['nA','xA','nB','xB'];
 if(fields.some(id=>$(id).value==='')){resultMessage(t.emptyResults);return;}
 const [nA,xA,nB,xB]=fields.map(id=>$(id).valueAsNumber),r=ABStats.observed(nA,xA,nB,xB);
 if(r.error){resultMessage(r.error==='sparse'?t.sparseResults:t.invalidCounts);return;}
 const metrics=document.createElement('div');metrics.className='result-metrics';
 for(const [label,value] of [[t.rates,`${pct(r.a)} / ${pct(r.b)}`],[t.absolute,pp(r.diff)],[t.pvalue,pformat(r.p)],[t.ci,`${pp(r.low)} … ${pp(r.high)}`]]){
  const cell=document.createElement('div'),small=document.createElement('small'),strong=document.createElement('strong');small.textContent=label;strong.textContent=value;cell.append(small,strong);metrics.append(cell);
 } $('result-output').append(metrics);
 if(r.srm<0.001){resultMessage(t.srm);return;}
 if(!$('complete').checked||!$('quality').checked){resultMessage(t.provisional);return;}
 if(saved.need!==undefined&&saved.need!==null&&Math.min(nA,nB)<saved.need){resultMessage(t.notEnoughActual);return;}
 resultMessage(r.p<0.05?t.significant:t.notSignificant);
}
['nA','xA','nB','xB','complete','quality'].forEach(id=>$(id).addEventListener('input',results));
$('unsupported').hidden=data.calculator_supported;$('scenario-fields').disabled=!data.calculator_supported;$('result-fields').disabled=!data.calculator_supported;$('export').disabled=!data.calculator_supported;
reset();results();
