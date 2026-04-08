import {Link, useNavigate} from 'react-router';
import {type MappedProductOptions} from '@shopify/hydrogen';
import type {
  Maybe,
  ProductOptionValueSwatch,
} from '@shopify/hydrogen/storefront-api-types';
import {AddToCartButton} from './AddToCartButton';
import {useAside} from './Aside';
import type {ProductFragment} from 'storefrontapi.generated';

export function ProductForm({
  productOptions,
  selectedVariant,
}: {
  productOptions: MappedProductOptions[];
  selectedVariant: ProductFragment['selectedOrFirstAvailableVariant'];
}) {
  const navigate = useNavigate();
  const {open} = useAside();
  return (
    <div className="product-form">
      {productOptions.map((option) => {
        if (option.optionValues.length === 1) return null;

        const selectedValue = option.optionValues.find((value) => value.selected);

        return (
          <div className="product-options" key={option.name}>
            <div className="product-options-header">
              <h5>{option.name}</h5>
              {selectedValue ? (
                <span className="product-options-selected">
                  {selectedValue.name}
                </span>
              ) : null}
            </div>
            <div className="product-options-grid">
              {option.optionValues.map((value) => {
                const {
                  name,
                  handle,
                  variantUriQuery,
                  selected,
                  available,
                  exists,
                  isDifferentProduct,
                  swatch,
                } = value;

                if (isDifferentProduct) {
                  return (
                    <Link
                      className="product-options-item"
                      key={option.name + name}
                      prefetch="intent"
                      preventScrollReset
                      replace
                      to={`/products/${handle}?${variantUriQuery}`}
                      style={{
                        border: selected
                          ? '1px solid #201710'
                          : '1px solid #dad0c7',
                        opacity: available ? 1 : 0.35,
                      }}
                    >
                      <ProductOptionSwatch
                        swatch={swatch}
                        name={name}
                        optionName={option.name}
                      />
                    </Link>
                  );
                }

                return (
                  <button
                    type="button"
                    className={`product-options-item${
                      exists && !selected ? ' link' : ''
                    }`}
                    key={option.name + name}
                    style={{
                      border: selected
                        ? '1px solid #201710'
                        : '1px solid #dad0c7',
                      opacity: available ? 1 : 0.35,
                    }}
                    disabled={!exists}
                    onClick={() => {
                      if (!selected) {
                        void navigate(`?${variantUriQuery}`, {
                          replace: true,
                          preventScrollReset: true,
                        });
                      }
                    }}
                  >
                    <ProductOptionSwatch
                      swatch={swatch}
                      name={name}
                      optionName={option.name}
                    />
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
      <AddToCartButton
        disabled={!selectedVariant || !selectedVariant.availableForSale}
        onClick={() => {
          open('cart');
        }}
        lines={
          selectedVariant
            ? [
                {
                  merchandiseId: selectedVariant.id,
                  quantity: 1,
                  selectedVariant,
                },
              ]
            : []
        }
      >
        {selectedVariant?.availableForSale ? 'Add to bag' : 'Sold out'}
      </AddToCartButton>
      <p className="product-form-note">
        Secure checkout with live shipping rates shown before payment.
      </p>
    </div>
  );
}

function ProductOptionSwatch({
  swatch,
  name,
  optionName,
}: {
  swatch?: Maybe<ProductOptionValueSwatch> | undefined;
  name: string;
  optionName: string;
}) {
  const image = swatch?.image?.previewImage?.url;
  const color = swatch?.color;
  const isColorOption = optionName.toLowerCase().includes('color');

  if (!isColorOption || (!image && !color)) {
    return <span className="product-option-label-text">{name}</span>;
  }

  return (
    <span className="product-option-swatch-wrap">
      <span
        aria-label={name}
        className="product-option-label-swatch"
        style={{
          backgroundColor: color || 'transparent',
        }}
      >
        {!!image && <img src={image} alt={name} />}
      </span>
      <span className="product-option-label-text">{name}</span>
    </span>
  );
}
