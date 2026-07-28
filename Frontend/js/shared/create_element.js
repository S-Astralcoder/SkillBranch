export function element(tag ="" , {id = "", text = "", classlist = [], atrributes = {} , childern = []} = {}) {
    const block = document.createElement(tag)
    if (block instanceof HTMLElement) {
        block.id = id
        if (text){
            block.textContent = text
        }
        if (classlist.length != 0){
            block.classList.add(...classlist)
        }
        for (const[key, value] of Object.entries(atrributes)){
            block.setAttribute(key, value)
        }
        for (const child of childern){
            block.appendChild(child)
        }
        return block
    }

}

