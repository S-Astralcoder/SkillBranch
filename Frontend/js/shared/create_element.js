export function element(tag ="" , {id = "", text = "", classlist = [], attributes = {} , children = []} = {}) {
    const block = document.createElement(tag)
    if (block instanceof HTMLElement) {
        if (id){block.id = id}
        if (text){
            block.textContent = text
        }
        if (classlist.length != 0){
            block.classList.add(...classlist)
        }
        for (const[key, value] of Object.entries(attributes)){
            block.setAttribute(key, value)
        }
        for (const child of children){
            block.appendChild(child)
        }
        return block
    }

}

