const $doc = document;
const $source_area =$doc.getElementById('source-area');
const $play_button = $doc.getElementById('play-programs');
const $out_area = $doc.getElementById('out-area')
const $in_area = $doc.getElementById('stdin-box');
const $answer_area =$doc.getElementById('answer-area');

const parentheses = (start, end, char)=>{
    $source_area.value = $source_area.value.substring(0,start) + char[0] + $source_area.value.substring(start, end)+ char[1]+ $source_area.value.substring(end);
    $source_area.selectionEnd = start +1
}

const lineStrToEnd = (str, end) =>{
    let i;
    for(i=end; str[i] != '\n' && i >=0; i--);
    if(i>0)return str.substring(i+1, end);
    else return str.substring(i, end);
}

$source_area.addEventListener('keydown',(e)=>{

    let start = $source_area.selectionStart;
    let end = $source_area.selectionEnd;
    let left_str = $source_area.value.substr(0,start);
    let right_str = $source_area.value.substr(end);

switch(e.key){
    case 'Tab':
        e.prevevtDefault();  //Tab移動の挙動を止める
        $source_area.value = left_str + '\t' +right_str;
        break;
    case '(':
        e.preventDefault(); //挙動を止める
        parentheses(start, end, '()');
        break;
    case '{':
        e.preventDefault();
        parentheses(start, end, '{}');
        break;
    case '[':
        e.preventDefault();
        parentheses(start, end, '[]');
        break;
    case '<':
        e.preventDefault();
        parentheses(start, end, '<>');
        break;
    case '"':
        e.preventDefault();
        parentheses(start, end, '""');
        break;
    case "'":
            e.preventDefault();
            parentheses(start, end, "'");
            break;
    }
});

$play_button.addEventListener('click',async()=>{
    $out_area.firstElementChild.textContent = 'loading...';
    console.log('input value : '+ $in_area.value);
   const res = await wandbox($source_area.value, $in_area.value);
   res.json().then((data)=>{
    console.log(data)
    if(data['status']==0){
        $out_area.firstElementChild.textContent = data['program_output'];
        $answer_area.firstElementChild.textContent = "正解";
    }
    else{
        $out_area.firstElementChild.textContent = data['compiler_error'];
        $answer_area.firstElementChild.textContent = "不正解";
    }
   }).catch((error)=>{
    console.log(error);
   });
});
