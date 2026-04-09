import {Money} from '@shopify/hydrogen';
import type {MoneyV2} from '@shopify/hydrogen/storefront-api-types';

export function ProductPrice({
  price,
  compareAtPrice,
}: {
  price?: MoneyV2;
  compareAtPrice?: MoneyV2 | null;
}) {
  return (
<>

 <div className="product-price">
       
    

    <div className="product-price">
      {compareAtPrice ? (
        <div className="product-price-on-sale">
          {price ? <Money data={price} /> : null}
          <s>
            <Money data={compareAtPrice} />
          </s>
        </div>
      ) : price ? (
        <Money data={price} />
      ) : (
        <span>&nbsp;</span>
      )}
    </div>

     <h3 className="text-emerald-600 font-semibold"> Loyalty Points: You could earn {Math.round(parseFloat(price.amount))} . </h3>
      <a href="/account/login"> Login In</a> or <a href="/account/register"> Register</a>
      </div>

    </>
  );
}
