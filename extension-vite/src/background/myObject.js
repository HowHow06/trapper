export class MyObject {
  constructor() {
    this.elements = {}
  }

  put(key, data) {
    if (data == null) {
      return false
    }

    this.elements[key] = data
    return true
  }

  size() {
    return Object.keys(this.elements).length
  }

  get(key) {
    return this.elements[key]
  }

  getObject() {
    return this.elements
  }

  hasKey(key) {
    return key in this.elements
  }

  delete(key) {
    delete this.elements[key]
    return true
  }

  print() {
    console.log(this.elements)
  }
}
