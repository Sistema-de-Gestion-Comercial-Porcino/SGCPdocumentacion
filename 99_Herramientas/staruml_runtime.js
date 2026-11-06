const fs=require('fs');
const BASE='/opt/StarUML/resources/app.asar';
const req=p=>require(BASE+'/'+p);
global.meta={};global.type={};Object.assign(global.type,req('src/core/graphics'),req('src/core/core')); 
global.app={type:global.type,preferences:{get:(k,d)=>d},getAppPath:()=>BASE};
app.metamodels=new (req('src/core/metamodel-manager'))();
app.metamodels.register(req('resources/default/metamodel.json'));
for(const e of ['uml','bpmn']){app.metamodels.register(req(`extensions/essential/${e}/metamodel.json`));req(`extensions/essential/${e}/elements.js`);}
app.repository=new (req('src/core/repository').Repository)();
const fi={regular:'Helvetica',bold:'Helvetica-Bold',italic:'Helvetica-Oblique',boldItalic:'Helvetica-BoldOblique',predefined:true};app.fontManager={getFontInfo:()=>fi,getDefaultFontInfo:()=>fi};
const PDFDocument=req('node_modules/pdfkit');
const {PDFCanvas}=req('src/engine/pdf-graphics');
async function render(diagram,path){
 let root=diagram;while(root._parent)root=root._parent;const did=diagram._id;app.repository.readObject(app.repository.writeObject(root));diagram=app.repository.get(did);
 const tmp=new PDFDocument({size:[100,100],margin:0});const c=new PDFCanvas(tmp);
 for(let i=0;i<3;i++)diagram.arrangeDiagram(c);
 const r=diagram.getBoundingBox(c);const w=Math.ceil(r.x2+35),h=Math.ceil(r.y2+35);
 const pdf=new PDFDocument({size:[w,h],margin:0,compress:true});const out=fs.createWriteStream(path);pdf.pipe(out);
 const cv=new PDFCanvas(pdf);diagram.drawDiagram(cv,false);pdf.end();tmp.end();
 await new Promise((res,rej)=>{out.on('finish',res);out.on('error',rej)});
 return {width:w,height:h};
}
module.exports={T:global.type,app,req,render};
if(require.main===module){const {T}=module.exports;let p=new T.Project();p.name='Prueba';let m=new T.UMLModel();m._parent=p;p.ownedElements.push(m);let d=new T.UMLClassDiagram();d.name='Test';d._parent=m;m.ownedElements.push(d);let cl=new T.UMLClass();cl.name='Cliente';cl._parent=m;m.ownedElements.push(cl);let v=new T.UMLClassView();v.model=cl;v._parent=d;v.left=40;v.top=40;v.width=200;v.height=100;d.ownedViews.push(v);render(d,'/tmp/staruml-test.pdf').then(x=>console.log(x));}
