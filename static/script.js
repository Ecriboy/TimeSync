// @ts-check

function show(element) {
    /** @type {HTMLElement}*/ (document.getElementById('dias')).innerHTML = element.getAttribute('name');

    setTimeout(function () {
        /** @type {HTMLElement}*/ (document.getElementById('dias')).innerHTML = '';
    }, 5000);
}


window.addEventListener("load", () => {
    let calendar = /** @type {HTMLElement} */ (document.getElementsByClassName("tabela")[0]);
    fitCalendarText(calendar);
    window.addEventListener("resize", () => fitCalendarText(calendar));
    let Groups = /** @type {HTMLElement} */ (document.getElementsByClassName("Grupos")[0]);
    FitGrupoText(Groups);
    window.addEventListener("resize", () => FitGrupoText(Groups));
    let defaultGroups = /** @type {HTMLElement} */ (document.getElementsByClassName("GruposEST")[0]).innerHTML;
    /** @type {HTMLElement}*/ (document.getElementById("GrupoTit")).addEventListener("input", ev => {
        let query = /** @type {HTMLInputElement}*/ (ev.target).value;
        search(query, defaultGroups);
    });
});

function FitGrupoText(Groups) {
    let element = [...Groups.getElementsByClassName("IT")];
    element.forEach(Alta => {
        /** @type {HTMLElement} */ (Alta).style.fontSize = Groups.clientWidth / 20 + "px";
    });
}

/** @param {HTMLElement} calendar */
function fitCalendarText(calendar) {
    let elements = [...calendar.getElementsByClassName("dias")];
    elements.push(...calendar.getElementsByClassName("fds"));
    elements.push(...calendar.getElementsByTagName("p"));
    /** @type {HTMLElement} */ (calendar.getElementsByClassName("corpo")[0]).style.display = "grid";
    /** @type {HTMLElement} */ (calendar.getElementsByClassName("tabela-est")[0]).style.display = "grid";
    let tableWidth = calendar.clientWidth;
    let bodyWidth = calendar.getElementsByClassName("corpo")[0].clientWidth;
    elements.forEach(dia => {
        /** @type {HTMLElement} */ (dia).style.fontSize = bodyWidth / 20 + "px";
    });
    /** @type {HTMLElement}*/ (document.getElementsByClassName("TitMes")[0]).style.fontSize =
        tableWidth / 20 + "px";
    /** @type {HTMLElement}*/ (document.getElementsByClassName("TitCal")[0]).style.fontSize =
        bodyWidth / 10 + "px";
    document.documentElement.style.setProperty(
        "--ball-size", bodyWidth / 15 + "px"
    );
}

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
    groupList.innerHTML = '<div class="AltaEST" style="width: 100%"><div class="MemNum"><div></div><div></div><p class="MemTit">Membros</p></div></div>';
    groups.forEach(group => {
        groupList.appendChild(group);
    })
}


