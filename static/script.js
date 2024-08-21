// @ts-check

function show(element) {
    /** @type {HTMLElement}*/ (document.getElementById('dias')).innerHTML = element.getAttribute('name');

    setTimeout(function () {
        /** @type {HTMLElement}*/ (document.getElementById('dias')).innerHTML = '';
    }, 5000);
}


window.addEventListener("load", () => {
    let defaultGroups = /** @type {HTMLElement} */ (document.getElementsByClassName("GruposEST")[0]).innerHTML;
    /** @type {HTMLElement}*/ (document.getElementById("GrupoTit")).addEventListener("input", ev => {
        let query = /** @type {HTMLInputElement}*/ (ev.target).value;
        search(query, defaultGroups);
    });
});

/** @param {string} query @param {string} defaultGroups */
function search(query, defaultGroups) {
    let groupList = /** @type {HTMLElement} */ (document.getElementsByClassName("GruposEST")[0]); 
    if(!query) {
        groupList.innerHTML = defaultGroups;
        return;
    }
    let groups = [...document.getElementsByClassName("GCont")].filter(group => {
        return group.getElementsByClassName("IT")[0].innerHTML.toUpperCase().includes(query.toUpperCase());
    }).sort((a, b) => {
        let aStarts = a.getElementsByClassName("IT")[0].innerHTML.toUpperCase().startsWith(query);
        let bStarts = b.getElementsByClassName("IT")[0].innerHTML.toUpperCase().startsWith(query);
        if(aStarts && bStarts || !aStarts && !bStarts) {
            return 0;
        }else if(aStarts) {
            return -1;
        }else {
            return 1;
        }
    });
    groupList.innerHTML = '<div class="AltaEST"><div class="MemNum"><p class="MemTit">Membros</p></div></div>';
    groups.forEach(group => {
        groupList.appendChild(group);
    })
}

