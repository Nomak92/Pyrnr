function createCodeBlock(textarea_target, save_target) {
    // Placeholder class that prevents the duplicate creation of
    // the same textarea when the collapsible is closed then reopened.
    if (!textarea_target.classList.contains("created")) {
            var editor = CodeMirror.fromTextArea(textarea_target, {
            lineNumbers : true,
            mode: "python",
            theme: "dracula",
            extraKeys: {
                "Tab": function(cm){
                    cm.replaceSelection("    " , "end");
                },
                "Ctrl-S": function(instance) {
                    $(save_target).trigger("click");
                },
                "Cmd-S": function(instance) {
                    $(save_target).trigger("click");
                }
            }});
        textarea_target.classList.toggle("created");
        setTimeout(function(){
            editor.refresh();
        },1);
    };
    return editor;
  }

async function setCodeBlock(cmeditor, promise){
    if (typeof promise === 'string'){
        cmeditor.setOption('value', promise);
    } else {
    let data = await promise.then(value =>{
        cmeditor.setOption('value', value);
    })};
    return cmeditor;
  }


async function runCode(data, csrftoken, url){
    return await postData(url = url, csrftoken = csrftoken, data = data).then(out => out.text().then(results => {
        return results;
    }));
}

async function saveCode(data, csrftoken, url){
    let results = await putData(url=url, csrftoken=csrftoken, data=data).then(out => out.text().then(results => {return results}));
    return results;
}

async function deleteCode(script_id, csrftoken, url){
    let results = await deleteData(id=script_id, csrftoken=csrftoken, url=url );
    return results;
}




function getcodeData(cm, script_id = '', script_name = ''){
    return {
        script_id: script_id,
        script_name: script_name,
        script_content: cm.getValue()
    };
}


async function postData(url = '', csrftoken = '', data = {}) {
    return await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
}

async function putData(url = '', csrftoken = '',  data = {}) {
    return await fetch(url, {
        method: 'PUT',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
}

async function getData(data = {}, csrftoken = '', url = ''  ) {
    return await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
}

async function deleteData(id = 0, csrftoken = '', url = ''){
    let data = {script_id: id};
    return await fetch(url, {
        method: 'DELETE',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });
}