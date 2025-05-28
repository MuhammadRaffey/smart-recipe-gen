from agents import (
    Agent,
    TResponseInputItem,
    GuardrailFunctionOutput,
    input_guardrail,
    Runner,
    RunContextWrapper,
    output_guardrail,
)
from dataclasses import dataclass

@dataclass
class IngredientsType:
    ingredients: list[str]
    is_halal: bool
    reason: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the ingredients are halal. Only Return false if the ingredients are not halal. if the user isnt asking about ingredients, return true.",
    output_type=IngredientsType,
    model="gpt-4o-mini",
)

@input_guardrail
async def ingredients_guardrail(ctx:RunContextWrapper[None],agent:Agent,input:str|list[TResponseInputItem])->GuardrailFunctionOutput:
    result=await Runner.run(
        guardrail_agent,
        input,
        context=ctx.context,
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_halal is False,
    )


