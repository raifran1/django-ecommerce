// Numbers in the input phone
const input_number = (e) => {
  var charCode = e.charCode ? e.charCode : e.keyCode;

  if (charCode < 48 || charCode > 57) {
    return false;
  }
}

// Mask of Number
const toPattern = (value, opts) => {
  var DIGIT = "9",
    pattern = (typeof opts === 'object' ? opts.pattern : opts),
    patternChars = pattern.replace(/\W/g, ''),
    output = pattern.split(""),
    values = value.toString().replace(/\W/g, ""),
    charsValues = values.replace(/\W/g, ''),
    index = 0,
    i,
    outputLength = output.length,
    placeholder = (typeof opts === 'object' ? opts.placeholder : undefined);

  for (i = 0; i < outputLength; i++) {
    if (index >= values.length) {
      if (patternChars.length == charsValues.length) {
        return output.join("");
      }
      else if ((placeholder !== undefined) && (patternChars.length > charsValues.length)) {
        return addPlaceholdersToOutput(output, i, placeholder).join("");
      }
      else {
        break;
      }
    }
    else{
      if ((output[i] === DIGIT && values[index].match(/[0-9]/))) {
        output[i] = values[index++];
      } else if (output[i] === DIGIT) {
        if(placeholder !== undefined){
          return addPlaceholdersToOutput(output, i, placeholder).join("");
        }
        else{
          return output.slice(0, i).join("");
        }
      } else if (output[i] === values[index]) {
        index++;
      }

    }
  }
    return output.join("").substr(0, i);
}

const unMask = value => value.replace(/\W/g, '')

const masker = (value, pattern, options) =>
  toPattern(value, { pattern, ...options })

const multimasker = (value, patterns, options) =>
  masker(
    value,
    patterns.reduce(
      (memo, pattern) => (value.length <= unMask(memo).length ? memo : pattern),
      patterns[0]
    ),
    options
  )

const mask = (value, pattern, options) =>
  typeof pattern === 'string' 
  ? masker(value, pattern || '', options) 
  : multimasker(value, pattern, options)


// Phones input events
const phones = [...document.querySelectorAll(".phone")];

phones.forEach(phone => {
  // mask phone
  phone.onkeypress = (e) => { return input_number(e) }

  // function for masker the phone number => | '(99) 99999-9999' |
  function mask_phone(e) {
    let phone_unMask = unMask(e.target.value)
    phone.value = mask(phone_unMask, '(99) 99999-9999')
  }
  phone.addEventListener('keyup', mask_phone)

});

