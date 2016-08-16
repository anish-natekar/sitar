//MainParser.cpp
#include"MainParser.h"
#include<cassert>

	//Constructor
	MainParser::MainParser()
	{
		_codeGenPtr=NULL;
		_globalDataPtr=NULL;
	};

	MainParser::~MainParser()
	{
		//std::cout<<"\nDestroying main parser\n\n";
	};



	void MainParser::setCodeGenPtr(CodeGen* code_gen)
	{
		_codeGenPtr=code_gen;
	};
	void MainParser::setGlobalDataPtr(GlobalData * global_data)
	{
		_globalDataPtr=global_data;
	};


	void MainParser::parse()
	{
		
		//check if all initializations have been done
		assert(_globalDataPtr!=NULL);
		assert(_codeGenPtr!=NULL);


		//Obtain name of input file:
		std::string input_file;
		input_file=_globalDataPtr->getAttribute("INPUT_FILE");
		if (input_file=="")
		{
			std::cerr<<"\nMain Parser Error: Name of Input file not specified";
			return;
		}
		finput=(pANTLR3_UINT8)(input_file.c_str());
		input = antlr3FileStreamNew ((pANTLR3_UINT8)finput, ANTLR3_ENC_8BIT);
		//input  =antlr3AsciiFileStreamNew(finput);
		if ( input == NULL)
		{
			fprintf(stderr, "Failed to open file %s\n", (char *)finput);
			exit(1);
		}
		lxr        = sitarLexerNew(input);     
		if ( lxr == NULL )
		{
			fprintf(stderr, "Unable to create the lexer due to malloc() failure1\n");
			exit(1);
		}

		tstream = antlr3CommonTokenStreamSourceNew(ANTLR3_SIZE_HINT, TOKENSOURCE(lxr));

		if (tstream == NULL)
		{
			fprintf(stderr, "Out of memory trying to allocate token stream\n");
			exit(1);
		}

		// Finally, now that we have our lexer constructed, we can create the parser
		//
		psr        = sitarParserNew(tstream);  // CParserNew is generated by ANTLR3

		if (psr == NULL)
		{
			fprintf(stderr, "Out of memory trying to allocate token stream\n");
			exit(1);
		}
		
	

		//Do some custom initializations
		psr->setCodeGenPtr(_codeGenPtr);
		psr->setGlobalDataPtr(_globalDataPtr);


		//Now start parsing
		psr->top(psr);



		//Free up everything

		if(psr!=NULL) 	{psr->free(psr); 	psr  = NULL;}
		if(tstream!=NULL)	{tstream ->free  (tstream);  	tstream = NULL;}
		if(lxr!=NULL)	{lxr->free(lxr);	lxr = NULL;}
		if(input!=NULL)		{input ->close (input);    input   = NULL;}

	};




