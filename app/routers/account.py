from .. import dependencies as dep
from bdantic import models
from fastapi import APIRouter, Depends
from typing import cast, Dict, List

router = APIRouter(prefix="/account", tags=["accounts"])


@router.get(
    "/",
    response_model=Dict[str, models.Account],
    summary="Fetch a list of all account names",
    response_description="A list of all account names.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def accounts(
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
) -> Dict[str, models.Account]:
    return beanfile.accounts


@router.get(
    "/{account_name}",
    response_model=models.Account,
    summary="Fetch the details of an account.",
    response_description="An `Account` containing the given account details.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def account(
    acct: models.Account = Depends(dep.get_account),
) -> models.Account:
    return acct


@router.get(
    "/{account_name}/balance",
    response_model=Dict[str, models.Inventory],
    summary="Fetch the balance of an account.",
    response_description="A mapping of currencies to lists of positions.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def balance(
    acct: models.Account = Depends(dep.get_account),
) -> Dict[str, models.Inventory]:
    return acct.balance


@router.get(
    "/{account_name}/transactions",
    response_model=List[models.Transaction],
    summary="Fetches all transactions associated with an account.",
    response_description="A list of transactions.",
    response_model_exclude_none=True,
    response_model_by_alias=True,
)
async def transactions(
    acct: models.Account = Depends(dep.get_account),
    beanfile: models.BeancountFile = Depends(dep.get_beanfile),
    mutator: dep.DirectivesMutator = Depends(dep.get_directives_mutator),
) -> List[models.Transaction]:
    txns = beanfile.entries.by_account(acct.name).by_type(models.Transaction)
    return cast(List[models.Transaction], mutator.mutate(txns).__root__)
