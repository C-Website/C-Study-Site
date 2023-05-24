let wandbox = async (source, input)=> {
    const param = {
        method: 'POST' ,
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify({
            code: source,
            stdin: input,
            options: "warning,gnu++1y",
            compiler: "gcc-head",
        })
    };
    return fetch("https://wandbox.org/api/compile.json",param)
}

let ex0_source = [
    '#include <stdio.h>',
    'int main()',
    '{',
    'return 0;',
    '}'
];